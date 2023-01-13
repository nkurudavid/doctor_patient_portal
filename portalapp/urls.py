from django.urls import path
from django.contrib.auth import views
from . import views

# from django.contrib import admin

urlpatterns = [
    # Home page urls
    path('', views.home, name='home'),
    # 
    
    # Patient urls
    path('patient/create_account', views.patientSignup, name='patientSignup'),
    path('patient/login', views.patientLogin, name='patientLogin'),
    path('patient/logout', views.patientLogout, name='patientLogout'),
    path('patient/', views.patientAccount, name='patientAccount'),
    path('patient/profile', views.patientProfile, name='patientProfile'),
    path('patient/profile/change_password', views.patientChangePassword, name='patientChangePassword'),
    path('patient/our_doctors', views.patientDoctorList, name='patientDoctorList'),
    path('patient/our_doctors/<int:pk>/details', views.patientDoctorDetails, name='patientDoctorDetails'),
    path('patient/medical_request', views.patientMedicalRequest, name='patientMedicalRequest'),
    path('patient/medical_request/<int:pk>/update_request', views.patientRequestDetails, name='patientRequestDetails'),
    path('patient/medical_request/<int:pk>/treatment', views.patientTreatment, name='patientTreatment'),
    # 
    
]
