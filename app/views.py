from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
from django.utils import timezone


def index(request):
    return render(request, 'app/index.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'app/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        User.objects.create(
            email=request.POST['email'],
            given_name=request.POST['given_name'],
            surname=request.POST['surname'],
            city=request.POST['city'],
            phone_number=request.POST['phone_number'],
            profile_description=request.POST.get('profile_description', ''),
            password=request.POST['password']
        )
        return redirect('user_list')
    return render(request, 'app/user_form.html', {'model_name': 'User', 'action': 'Create'})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.email = request.POST['email']
        user.given_name = request.POST['given_name']
        user.surname = request.POST['surname']
        user.city = request.POST['city']
        user.phone_number = request.POST['phone_number']
        user.profile_description = request.POST.get('profile_description', '')
        user.password = request.POST['password']
        user.save()
        return redirect('user_list')
    return render(request, 'app/user_form.html', {'model_name': 'User', 'action': 'Update', 'user': user})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'app/delete_confirm.html', {'object': user, 'model_name': 'User'})


def caregiver_list(request):
    caregivers = Caregiver.objects.all()
    return render(request, 'app/caregiver_list.html', {'caregivers': caregivers})


def caregiver_create(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.POST['caregiver_user'])
        Caregiver.objects.create(
            caregiver_user=user,
            photo=request.POST.get('photo', ''),
            gender=request.POST['gender'],
            caregiving_type=request.POST['caregiving_type'],
            hourly_rate=request.POST['hourly_rate']
        )
        return redirect('caregiver_list')
    users = User.objects.all()
    return render(request, 'app/caregiver_form.html', {'model_name': 'Caregiver', 'action': 'Create', 'users': users})


def caregiver_update(request, pk):
    caregiver = get_object_or_404(Caregiver, pk=pk)
    if request.method == 'POST':
        caregiver.photo = request.POST.get('photo', '')
        caregiver.gender = request.POST['gender']
        caregiver.caregiving_type = request.POST['caregiving_type']
        caregiver.hourly_rate = request.POST['hourly_rate']
        caregiver.save()
        return redirect('caregiver_list')
    users = User.objects.all()
    return render(request, 'app/caregiver_form.html', {'model_name': 'Caregiver', 'action': 'Update', 'caregiver': caregiver, 'users': users})


def caregiver_delete(request, pk):
    caregiver = get_object_or_404(Caregiver, pk=pk)
    if request.method == 'POST':
        caregiver.delete()
        return redirect('caregiver_list')
    return render(request, 'app/delete_confirm.html', {'object': caregiver, 'model_name': 'Caregiver'})


def member_list(request):
    members = Member.objects.all()
    return render(request, 'app/member_list.html', {'members': members})


def member_create(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.POST['member_user'])
        Member.objects.create(
            member_user=user,
            house_rules=request.POST.get('house_rules', ''),
            dependent_description=request.POST.get('dependent_description', '')
        )
        return redirect('member_list')
    users = User.objects.all()
    return render(request, 'app/member_form.html', {'model_name': 'Member', 'action': 'Create', 'users': users})


def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.house_rules = request.POST.get('house_rules', '')
        member.dependent_description = request.POST.get('dependent_description', '')
        member.save()
        return redirect('member_list')
    users = User.objects.all()
    return render(request, 'app/member_form.html', {'model_name': 'Member', 'action': 'Update', 'member': member, 'users': users})


def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'app/delete_confirm.html', {'object': member, 'model_name': 'Member'})


def address_list(request):
    addresses = Address.objects.all()
    return render(request, 'app/address_list.html', {'addresses': addresses})


def address_create(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=request.POST['member_user'])
        Address.objects.create(
            member_user=member,
            house_number=request.POST.get('house_number', ''),
            street=request.POST.get('street', ''),
            town=request.POST.get('town', '')
        )
        return redirect('address_list')
    members = Member.objects.all()
    return render(request, 'app/address_form.html', {'model_name': 'Address', 'action': 'Create', 'members': members})


def address_update(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        address.house_number = request.POST.get('house_number', '')
        address.street = request.POST.get('street', '')
        address.town = request.POST.get('town', '')
        address.save()
        return redirect('address_list')
    members = Member.objects.all()
    return render(request, 'app/address_form.html', {'model_name': 'Address', 'action': 'Update', 'address': address, 'members': members})


def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'app/delete_confirm.html', {'object': address, 'model_name': 'Address'})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'app/job_list.html', {'jobs': jobs})


def job_create(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=request.POST['member_user'])
        Job.objects.create(
            member_user=member,
            required_caregiving_type=request.POST['required_caregiving_type'],
            other_requirements=request.POST.get('other_requirements', ''),
            date_posted=timezone.now()
        )
        return redirect('job_list')
    members = Member.objects.all()
    return render(request, 'app/job_form.html', {'model_name': 'Job', 'action': 'Create', 'members': members})


def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.member_user = get_object_or_404(Member, pk=request.POST['member_user'])
        job.required_caregiving_type = request.POST['required_caregiving_type']
        job.other_requirements = request.POST.get('other_requirements', '')
        job.save()
        return redirect('job_list')
    members = Member.objects.all()
    return render(request, 'app/job_form.html', {'model_name': 'Job', 'action': 'Update', 'job': job, 'members': members})


def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'app/delete_confirm.html', {'object': job, 'model_name': 'Job'})


def jobapplication_list(request):
    applications = JobApplication.objects.all()
    return render(request, 'app/jobapplication_list.html', {'applications': applications})


def jobapplication_create(request):
    if request.method == 'POST':
        caregiver = get_object_or_404(Caregiver, pk=request.POST['caregiver_user'])
        job = get_object_or_404(Job, pk=request.POST['job'])
        JobApplication.objects.create(
            caregiver_user=caregiver,
            job=job,
            date_applied=timezone.now()
        )
        return redirect('jobapplication_list')
    caregivers = Caregiver.objects.all()
    jobs = Job.objects.all()
    return render(request, 'app/jobapplication_form.html', {'model_name': 'JobApplication', 'action': 'Create', 'caregivers': caregivers, 'jobs': jobs})


def jobapplication_update(request, caregiver_id, job_id):
    application = get_object_or_404(JobApplication, caregiver_user_id=caregiver_id, job_id=job_id)
    if request.method == 'POST':
        application.caregiver_user = get_object_or_404(Caregiver, pk=request.POST['caregiver_user'])
        application.job = get_object_or_404(Job, pk=request.POST['job'])
        application.save()
        return redirect('jobapplication_list')
    caregivers = Caregiver.objects.all()
    jobs = Job.objects.all()
    return render(request, 'app/jobapplication_form.html', {'model_name': 'JobApplication', 'action': 'Update', 'application': application, 'caregivers': caregivers, 'jobs': jobs})


def jobapplication_delete(request, caregiver_id, job_id):
    application = get_object_or_404(JobApplication, caregiver_user_id=caregiver_id, job_id=job_id)
    if request.method == 'POST':
        application.delete()
        return redirect('jobapplication_list')
    return render(request, 'app/delete_confirm.html', {'object': application, 'model_name': 'JobApplication'})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'app/appointment_list.html', {'appointments': appointments})


def appointment_create(request):
    if request.method == 'POST':
        caregiver = get_object_or_404(Caregiver, pk=request.POST['caregiver_user'])
        member = get_object_or_404(Member, pk=request.POST['member_user'])
        Appointment.objects.create(
            caregiver_user=caregiver,
            member_user=member,
            appointment_date=request.POST['appointment_date'],
            appointment_time=request.POST['appointment_time'],
            work_hours=request.POST['work_hours'],
            status=request.POST.get('status', 'pending')
        )
        return redirect('appointment_list')
    caregivers = Caregiver.objects.all()
    members = Member.objects.all()
    return render(request, 'app/appointment_form.html', {'model_name': 'Appointment', 'action': 'Create', 'caregivers': caregivers, 'members': members})


def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.caregiver_user = get_object_or_404(Caregiver, pk=request.POST['caregiver_user'])
        appointment.member_user = get_object_or_404(Member, pk=request.POST['member_user'])
        appointment.appointment_date = request.POST['appointment_date']
        appointment.appointment_time = request.POST['appointment_time']
        appointment.work_hours = request.POST['work_hours']
        appointment.status = request.POST.get('status', 'pending')
        appointment.save()
        return redirect('appointment_list')
    caregivers = Caregiver.objects.all()
    members = Member.objects.all()
    return render(request, 'app/appointment_form.html', {'model_name': 'Appointment', 'action': 'Update', 'appointment': appointment, 'caregivers': caregivers, 'members': members})


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'app/delete_confirm.html', {'object': appointment, 'model_name': 'Appointment'})
