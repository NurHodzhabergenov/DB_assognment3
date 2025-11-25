from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    path('caregivers/', views.caregiver_list, name='caregiver_list'),
    path('caregivers/create/', views.caregiver_create, name='caregiver_create'),
    path('caregivers/<int:pk>/update/', views.caregiver_update, name='caregiver_update'),
    path('caregivers/<int:pk>/delete/', views.caregiver_delete, name='caregiver_delete'),
    
    path('members/', views.member_list, name='member_list'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:pk>/update/', views.member_update, name='member_update'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/<int:pk>/update/', views.address_update, name='address_update'),
    path('addresses/<int:pk>/delete/', views.address_delete, name='address_delete'),
    
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/update/', views.job_update, name='job_update'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    
    path('job-applications/', views.jobapplication_list, name='jobapplication_list'),
    path('job-applications/create/', views.jobapplication_create, name='jobapplication_create'),
    path('job-applications/<int:caregiver_id>/<int:job_id>/update/', views.jobapplication_update, name='jobapplication_update'),
    path('job-applications/<int:caregiver_id>/<int:job_id>/delete/', views.jobapplication_delete, name='jobapplication_delete'),
    
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]

