from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(unique=True, max_length=30)
    profile_description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'


class Caregiver(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    CAREGIVING_TYPE_CHOICES = [
        ('babysitter', 'Babysitter'),
        ('elderly_caregiver', 'Elderly Caregiver'),
        ('playmate', 'Playmate'),
    ]
    
    caregiver_user = models.OneToOneField('User', models.CASCADE, primary_key=True, db_column='caregiver_user_id')
    photo = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    caregiving_type = models.CharField(max_length=20, choices=CAREGIVING_TYPE_CHOICES)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'caregiver'


class Member(models.Model):
    member_user = models.OneToOneField('User', models.CASCADE, primary_key=True, db_column='member_user_id')
    house_rules = models.TextField(blank=True, null=True)
    dependent_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'member'


class Address(models.Model):
    member_user = models.OneToOneField('Member', models.CASCADE, primary_key=True, db_column='member_user_id')
    house_number = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'address'


class Job(models.Model):
    CAREGIVING_TYPE_CHOICES = [
        ('babysitter', 'Babysitter'),
        ('elderly_caregiver', 'Elderly Caregiver'),
        ('playmate', 'Playmate'),
    ]
    
    job_id = models.AutoField(primary_key=True)
    member_user = models.ForeignKey('Member', models.CASCADE, db_column='member_user_id')
    required_caregiving_type = models.CharField(max_length=20, choices=CAREGIVING_TYPE_CHOICES)
    other_requirements = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField()

    class Meta:
        db_table = 'job'


class JobApplication(models.Model):
    caregiver_user = models.ForeignKey('Caregiver', models.CASCADE, db_column='caregiver_user_id', primary_key=True)
    job = models.ForeignKey('Job', models.CASCADE, db_column='job_id')
    date_applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'job_application'
        unique_together = (('caregiver_user', 'job'),)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined'),
    ]
    
    appointment_id = models.AutoField(primary_key=True)
    caregiver_user = models.ForeignKey('Caregiver', models.CASCADE, db_column='caregiver_user_id')
    member_user = models.ForeignKey('Member', models.CASCADE, db_column='member_user_id')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    work_hours = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'appointment'
