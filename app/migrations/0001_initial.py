import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('given_name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=30, unique=True)),
                ('profile_description', models.TextField(blank=True, null=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Caregiver',
            fields=[
                ('caregiver_user', models.OneToOneField(db_column='caregiver_user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.user')),
                ('photo', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20)),
                ('caregiving_type', models.CharField(choices=[('babysitter', 'Babysitter'), ('elderly_caregiver', 'Elderly Caregiver'), ('playmate', 'Playmate')], max_length=20)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'db_table': 'caregiver',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_user', models.OneToOneField(db_column='member_user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.user')),
                ('house_rules', models.TextField(blank=True, null=True)),
                ('dependent_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('member_user', models.OneToOneField(db_column='member_user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.member')),
                ('house_number', models.CharField(blank=True, max_length=50, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.AutoField(primary_key=True, serialize=False)),
                ('required_caregiving_type', models.CharField(choices=[('babysitter', 'Babysitter'), ('elderly_caregiver', 'Elderly Caregiver'), ('playmate', 'Playmate')], max_length=20)),
                ('other_requirements', models.TextField(blank=True, null=True)),
                ('date_posted', models.DateTimeField()),
                ('member_user', models.ForeignKey(db_column='member_user_id', on_delete=django.db.models.deletion.CASCADE, to='app.member')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('work_hours', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('caregiver_user', models.ForeignKey(db_column='caregiver_user_id', on_delete=django.db.models.deletion.CASCADE, to='app.caregiver')),
                ('member_user', models.ForeignKey(db_column='member_user_id', on_delete=django.db.models.deletion.CASCADE, to='app.member')),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('caregiver_user', models.ForeignKey(db_column='caregiver_user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.caregiver')),
                ('job', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='app.job')),
                ('date_applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'job_application',
                'managed': False,
                'unique_together': {('caregiver_user', 'job')},
            },
        ),
    ]
