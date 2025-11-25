from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Numeric, ForeignKey,
    Date, Time, Enum, DateTime, func, update, delete, select, case, text
)
from sqlalchemy.orm import declarative_base, relationship, Session, joinedload, aliased

Base = declarative_base()

gender_enum = Enum("male", "female", name="gender_enum")
caregiving_type_enum = Enum(
    "babysitter", "elderly_caregiver", "playmate", name="caregiving_type_enum"
)
appointment_status_enum = Enum(
    "pending", "confirmed", "declined", name="appointment_status_enum"
)

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(30), nullable=False, unique=True)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

    caregiver = relationship("Caregiver", back_populates="user", uselist=False)
    member = relationship("Member", back_populates="user", uselist=False)


class Caregiver(Base):
    __tablename__ = "caregiver"

    caregiver_user_id = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    photo = Column(Text)
    gender = Column(gender_enum, nullable=False)
    caregiving_type = Column(caregiving_type_enum, nullable=False)
    hourly_rate = Column(Numeric(8, 2), nullable=False)

    user = relationship("User", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver")


class Member(Base):
    __tablename__ = "member"

    member_user_id = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    house_rules = Column(Text)
    dependent_description = Column(Text)

    user = relationship("User", back_populates="member")
    addresses = relationship("Address", back_populates="member")
    jobs = relationship("Job", back_populates="member")
    appointments = relationship("Appointment", back_populates="member")


class Address(Base):
    __tablename__ = "address"

    member_user_id = Column(
        Integer,
        ForeignKey("member.member_user_id", ondelete="CASCADE"),
        primary_key=True
    )
    house_number = Column(String(50))
    street = Column(String(255))
    town = Column(String(100))

    member = relationship("Member", back_populates="addresses")


class Job(Base):
    __tablename__ = "job"

    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(
        Integer,
        ForeignKey("member.member_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    required_caregiving_type = Column(caregiving_type_enum, nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(DateTime, server_default=func.now(), nullable=False)

    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_application"

    caregiver_user_id = Column(
        Integer,
        ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    job_id = Column(
        Integer,
        ForeignKey("job.job_id", ondelete="CASCADE"),
        primary_key=True,
    )
    date_applied = Column(DateTime, server_default=func.now(), nullable=False)

    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")


class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(
        Integer,
        ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    member_user_id = Column(
        Integer,
        ForeignKey("member.member_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Integer, nullable=False)
    status = Column(appointment_status_enum, nullable=False, server_default="pending")

    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")


DATABASE_URL = "postgresql+psycopg2://daserutorre:123@localhost:5432/caregiver_db"

engine = create_engine(DATABASE_URL, echo=False)


def task_3_1_update_arman_phone(session: Session):
    stmt = (
        update(User)
        .where(User.given_name == "Arman", User.surname == "Armanov")
        .values(phone_number="+77773414141")
    )
    session.execute(stmt)
    session.commit()


def task_3_2_update_caregiver_commission(session: Session):
    stmt = (
        update(Caregiver)
        .values(
            hourly_rate=case(
                (Caregiver.hourly_rate < 10, Caregiver.hourly_rate + 0.3),
                else_=Caregiver.hourly_rate * 1.1,
            )
        )
    )
    session.execute(stmt)
    session.commit()


def task_4_1_delete_jobs_by_amina(session: Session):
    subq_member_ids = (
        select(Member.member_user_id)
        .join(User, Member.member_user_id == User.user_id)
        .where(User.given_name == "Amina", User.surname == "Aminova")
    )

    stmt = delete(Job).where(Job.member_user_id.in_(subq_member_ids))
    session.execute(stmt)
    session.commit()


def task_4_2_delete_members_on_kabanbay(session: Session):
    subq_member_ids = (
        select(Address.member_user_id)
        .where(Address.street == "Kabanbay Batyr")
    )

    stmt = delete(Member).where(Member.member_user_id.in_(subq_member_ids))
    session.execute(stmt)
    session.commit()


def task_5_1_caregiver_member_names_for_confirmed(session: Session):
    caregiver_user = aliased(User, name="caregiver_user")
    member_user = aliased(User, name="member_user")

    stmt = (
        select(
            Appointment.appointment_id,
            caregiver_user.given_name.label("caregiver_name"),
            caregiver_user.surname.label("caregiver_surname"),
            member_user.given_name.label("member_name"),
            member_user.surname.label("member_surname"),
        )
        .join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .join(caregiver_user, caregiver_user.user_id == Caregiver.caregiver_user_id)
        .join(Member, Appointment.member_user_id == Member.member_user_id)
        .join(member_user, member_user.user_id == Member.member_user_id)
        .where(Appointment.status == "confirmed")
    )

    for row in session.execute(stmt):
        print(row)


def task_5_2_job_ids_with_soft_spoken(session: Session):
    stmt = select(Job.job_id).where(Job.other_requirements.ilike("%soft-spoken%"))
    for row in session.execute(stmt):
        print(row.job_id)


def task_5_3_work_hours_babysitter_positions(session: Session):
    stmt = (
        select(Appointment.appointment_id, Appointment.work_hours)
        .join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .where(Caregiver.caregiving_type == "babysitter")
    )

    for row in session.execute(stmt):
        print(f"Appointment {row.appointment_id}: {row.work_hours} hours")


def task_5_4_members_elderly_care_astana_no_pets(session: Session):
    stmt = (
        select(User.given_name, User.surname)
        .select_from(Member)
        .join(User, Member.member_user_id == User.user_id)
        .join(Job, Job.member_user_id == Member.member_user_id)
        .where(
            Job.required_caregiving_type == "elderly_caregiver",
            User.city == "Astana",
            Member.house_rules.ilike("%No pets.%"),
        )
        .distinct()
    )

    for row in session.execute(stmt):
        print(row.given_name, row.surname)


def task_6_1_count_applicants_per_job(session: Session):
    stmt = (
        select(
            Job.job_id,
            func.count(JobApplication.caregiver_user_id).label("num_applicants"),
        )
        .outerjoin(JobApplication, Job.job_id == JobApplication.job_id)
        .group_by(Job.job_id)
        .order_by(Job.job_id)
    )

    for row in session.execute(stmt):
        print(f"Job {row.job_id}: {row.num_applicants} applicants")


def task_6_2_total_hours_per_caregiver(session: Session):
    stmt = (
        select(
            User.given_name,
            User.surname,
            func.sum(Appointment.work_hours).label("total_hours"),
        )
        .select_from(Caregiver)
        .join(User, User.user_id == Caregiver.caregiver_user_id)
        .join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .where(Appointment.status == "confirmed")
        .group_by(User.given_name, User.surname)
        .order_by(User.surname, User.given_name)
    )

    for row in session.execute(stmt):
        print(f"{row.given_name} {row.surname}: {row.total_hours} hours")


def task_6_3_average_pay_per_caregiver(session: Session):
    avg_pay_expr = func.avg(Caregiver.hourly_rate * Appointment.work_hours)

    stmt = (
        select(
            User.given_name,
            User.surname,
            avg_pay_expr.label("avg_pay"),
        )
        .select_from(Caregiver)
        .join(User, User.user_id == Caregiver.caregiver_user_id)
        .join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .where(Appointment.status == "confirmed")
        .group_by(User.given_name, User.surname)
        .order_by(User.surname, User.given_name)
    )

    for row in session.execute(stmt):
        print(f"{row.given_name} {row.surname}: avg pay {row.avg_pay}")


def task_6_4_caregivers_above_average_earnings(session: Session):
    caregiver_pay_subq = (
        select(
            Caregiver.caregiver_user_id.label("cid"),
            func.sum(Caregiver.hourly_rate * Appointment.work_hours).label("total_pay"),
        )
        .join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .where(Appointment.status == "confirmed")
        .group_by(Caregiver.caregiver_user_id)
        .subquery()
    )

    overall_avg = select(func.avg(caregiver_pay_subq.c.total_pay))

    stmt = (
        select(
            User.given_name,
            User.surname,
            caregiver_pay_subq.c.total_pay,
        )
        .join(Caregiver, Caregiver.caregiver_user_id == caregiver_pay_subq.c.cid)
        .join(User, User.user_id == Caregiver.caregiver_user_id)
        .where(
            caregiver_pay_subq.c.total_pay > overall_avg.scalar_subquery()
        )
        .order_by(caregiver_pay_subq.c.total_pay.desc())
    )

    for row in session.execute(stmt):
        print(f"{row.given_name} {row.surname}: total pay {row.total_pay}")


def task_7_total_cost_per_caregiver(session: Session):
    stmt = (
        select(
            User.given_name,
            User.surname,
            func.sum(Caregiver.hourly_rate * Appointment.work_hours).label("total_cost"),
        )
        .select_from(Caregiver)
        .join(User, User.user_id == Caregiver.caregiver_user_id)
        .join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)
        .where(Appointment.status == "confirmed")
        .group_by(User.given_name, User.surname)
        .order_by(User.surname, User.given_name)
    )

    for row in session.execute(stmt):
        print(f"{row.given_name} {row.surname}: total cost {row.total_cost}")


def task_8_create_and_view_job_applications(session: Session):
    create_view_sql = """
        CREATE OR REPLACE VIEW job_applications_view AS
        SELECT
            ja.job_id,
            j.other_requirements,
            ja.caregiver_user_id,
            u.given_name AS caregiver_name,
            u.surname    AS caregiver_surname
        FROM job_application ja
        JOIN job j
          ON j.job_id = ja.job_id
        JOIN caregiver c
          ON c.caregiver_user_id = ja.caregiver_user_id
        JOIN "user" u
          ON u.user_id = c.caregiver_user_id;
    """
    session.execute(text(create_view_sql))
    session.commit()

    stmt = text("SELECT * FROM job_applications_view ORDER BY job_id, caregiver_user_id;")
    for row in session.execute(stmt):
        print(row)


def main():
        with Session(engine) as session:
            task_3_1_update_arman_phone(session)
            task_3_2_update_caregiver_commission(session)
            task_4_1_delete_jobs_by_amina(session)
            task_4_2_delete_members_on_kabanbay(session)
            task_5_1_caregiver_member_names_for_confirmed(session)
            task_5_2_job_ids_with_soft_spoken(session)
            task_5_3_work_hours_babysitter_positions(session)
            task_5_4_members_elderly_care_astana_no_pets(session)
            task_6_1_count_applicants_per_job(session)
            task_6_2_total_hours_per_caregiver(session)
            task_6_3_average_pay_per_caregiver(session)
            task_6_4_caregivers_above_average_earnings(session)
            task_7_total_cost_per_caregiver(session)
            task_8_create_and_view_job_applications(session)


if __name__ == "__main__":
    main()
