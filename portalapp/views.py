import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from portalapp.models import *
# Create your views here.


def home(request):
    # GET ALL DATA IN DOCTOR MODEL
    doctorData = Doctor.objects.all().order_by('speciality')
    found_doctorData =doctorData.count()

    context = {
        'doctors': doctorData,
        'count_doctor': found_doctorData,
        }
    return render(request, 'portalapp/home.html', context)


def patientSignup(request):
    if request.method == 'POST' :
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if not (
            fname and lname and email and phone and dob and gender and address and pass1 and pass2
            ) : 
            messages.warning(request, "Error , All fields are required.")
            return redirect(patientSignup) 
        
        else :
            #CHECK FOR EXISTING EMAIL
            if get_user_model().objects.filter(email=email,):
                messages.warning(request, "Email already exist! Try again ...")
                return redirect(patientSignup)
            
            #CHECK FOR EXISTING PHONE NUMBER
            elif Patient.objects.filter(phone=phone,):
                messages.warning(request, "Phone number already exist! Try again ...")
                return redirect(patientSignup)
                
            # VERIFYING THE PASSWORD
            elif len(pass1) < 5:
                messages.warning(request, "Your password is too weak!")
                return redirect(patientSignup)
            
            elif pass1 != pass2 :
                messages.error(request, "Error , Password don't match!")
                return redirect(patientSignup)
            
            else: 
                # CREATE USER FOR PATIENT
                user =  get_user_model().objects.create_user(
                    first_name=fname.upper(),
                    last_name=lname.upper(),
                    email=email.lower(), 
                    userType="Patient", 
                    password=pass1
                )

                if user:
                    patientUser =  get_user_model().objects.get(email=email)
                    # INSERT PATIENT DATA IN PATIENT MODEL
                    add_patient = Patient(
                        user = patientUser,
                        gender = gender.upper(),
                        birthdate = dob, 
                        phone = phone, 
                        address = address.upper(),
                    )
                    add_patient.save()
                        
                    messages.success(request, "You are registered successfully.")
                    return redirect(patientLogin)
        
    else:
        context = {'title': 'Patient Register',}
        return render(request, 'portalapp/patient/register.html', context)


def patientLogin(request):
    if not request.user.is_authenticated or request.user.userType !='Patient':
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None and user.userType =='Patient':
                login(request, user)
                messages.success(request, ('You are now logged in.'))
                return redirect(patientAccount)
            
            else:
                messages.error(request, ('User Email or Password is not correct! Try again...'))
                return redirect(patientLogin)
            
        else:
            context = {'title': 'Patient Login', }
            return render(request, 'portalapp/patient/login.html', context)

    else:
        return redirect(patientAccount)
    

@login_required(login_url='patientLogin')
def patientLogout(request):
    # USER LOG OUT
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientAccount(request):
    if request.user.is_authenticated and request.user.userType =='Patient':

        myPatient = Patient.objects.get(user=request.user)
        # GET ALL ALL TREATMENT REQUEST IN ILLNESS MODEL
        myRequestsData = Illness.objects.filter(patient=myPatient)
        found_requestData = myRequestsData.count()
        
        # GET ALL DATA IN DOCTOR MODEL
        doctorData = Doctor.objects.all().order_by('speciality')
        found_doctorData =doctorData.count()

        context = {
            'title': 'Patient Account',
            'requests': myRequestsData,
            'request_count': found_requestData,
            'doctors': doctorData,
            'count_doctor': found_doctorData,
            'home_active': 'active',
        }
        return render(request, 'portalapp/patient/dashboard.html', context)
    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientChangePassword(request):
    if request.user.is_authenticated and request.user.userType =='Patient':
        if request.method == 'POST':
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email= request.user.email)
                
                if not user.check_password(old_password):
                    messages.error(request, "Your old password is not correct!")
                    return redirect(patientChangePassword)
        
                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(patientChangePassword)

                    elif new_password != confirmed_new_password:
                        messages.error(request, "Your new password not match the confirm password !")
                        return redirect(patientChangePassword)
                        
                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(request, "Your password has been changed successfully.!")
                        return redirect(patientChangePassword)
                                
            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(patientChangePassword)

        else:
            context = {'title': 'Patient Change Password',}
            return render(request, 'portalapp/patient/change-password.html', context)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientProfile(request):
    if request.user.is_authenticated and request.user.userType =='Patient':
        if request.method == 'POST' :
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            address = request.POST.get('address')

            if not (
                fname and lname and phone and dob and gender and address
                ) : 
                messages.warning(request, "Error , All fields are required.")
                return redirect(patientProfile) 
            
            else :
                #CHECK FOR EXISTING PHONE
                if Patient.objects.filter(phone=phone,).exclude(user=request.user,):
                    messages.warning(request, "Phone number already exist! Try again ...")
                    return redirect(patientProfile)
                
                else:
                    # GET THE USER ROW
                    userUpdate = get_user_model().objects.filter(email=request.user.email).update(
                        first_name = fname,
                        last_name = lname,
                    ) 
                    # GET THE USER ROW
                    profileUpdate = Patient.objects.filter(user=request.user).update(
                        gender = gender,
                        birthdate = dob,
                        phone = phone,
                        address = address,
                    ) 

                    if userUpdate and profileUpdate:
                        messages.success(request, "Profile updated successfully.")
                        return redirect(patientProfile)
            
        else:
            profileData = Patient.objects.get(user=request.user)
            context = {
                'title': 'Patient Profile',
                'patientProfile': profileData,
            }
            return render(request, 'portalapp/patient/profile.html', context)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientDoctorList(request):
    if request.user.is_authenticated and request.user.userType =='Patient':
        # GET ALL DATA IN DOCTOR MODEL
        doctorData = Doctor.objects.all().order_by('speciality')
            
        context = {
            'title': 'Patient Doctor List',
            'doctors': doctorData,
            'doctorList_active': 'active',
        }
        return render(request, 'portalapp/patient/doctors-list.html', context)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientDoctorDetails(request, pk):
    if request.user.is_authenticated and request.user.userType =='Patient':
        
        if Doctor.objects.filter(id=pk).exists() :
            # GET DOCTOR DETAILS FROM DOCTOR MODEL
            doctorData = Doctor.objects.get(id=pk)
            
            context = {
                'title': 'Patient Doctor Details',
                'doctor': doctorData,
                'doctorList_active': 'active',
                }
            return render(request, 'portalapp/patient/doctor_profile.html', context)

        else:
            return redirect(patientDoctorList)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientMedicalRequest(request):
    if request.user.is_authenticated and request.user.userType =='Patient':

        myPatient = Patient.objects.get(user=request.user)

        if request.method == 'POST' :
            illnesDescript = request.POST.get('description')

            if not (illnesDescript) : 
                messages.warning(request, "Error , Field is required.")
                return redirect(patientMedicalRequest) 
            
            else :
                # INSERT PATIENT DATA IN PATIENT MODEL
                add_illnesDescript = Illness(
                    patient = myPatient,
                    description = illnesDescript,
                    status = "Waiting",
                )
                add_illnesDescript.save() 
                
                # UPDATE THE REQUEST TIMER MODEL
                requestData =  Illness.objects.filter(patient=myPatient).latest('id')

                add_requestTimer = requestTimer(
                    request = requestData,
                    start_period = requestData.date_created,
                    # SETTING THE 5hr FOR TIMER
                    end_period = requestData.date_created + datetime.timedelta(hours = 5),
                )
                add_requestTimer.save()

                messages.success(request, "Your request submitted successfully.")
                return redirect(patientMedicalRequest)

        else:
            # GET ALL ALL TREATMENT REQUEST IN ILLNESS MODEL
            myRequestsData = Illness.objects.filter(patient=myPatient)
            found_requestData = myRequestsData.count()

            context = {
                'title': 'Patient Account',
                'requests': myRequestsData,
                'request_count': found_requestData,
                'medical_request_active': 'active',
            }
            return render(request, 'portalapp/patient/medical_request.html', context)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)

@login_required(login_url='patientLogin')
def patientTreatment(request, pk):
    if request.user.is_authenticated and request.user.userType =='Patient':
        
        patientUser =  Patient.objects.get(user=request.user)
        if Illness.objects.filter(patient=patientUser, id=pk).exists() :
            # GET PATIENT REQUEST FROM ILLNESS MODEL
            patientRequest = Illness.objects.get(patient=patientUser, id=pk)

            # GET ALL TREATMENT  FROM Treatment MODEL
            treatment = Treatment.objects.filter(illness=patientRequest,)
                
            # GET ALL DATA IN DOCTOR MODEL
            doctorData = Doctor.objects.all().order_by('speciality')
            found_doctorData =doctorData.count()

            # GET REQUEST TIMER FROM requestTimer MODEL
            reqTimer = requestTimer.objects.get(request=patientRequest,)

            context = {
                'title': 'Patient Doctor Details',
                'request': patientRequest,
                'illnessTreatment': treatment,
                'doctors': doctorData,
                'count_doctor': found_doctorData,
                'reqTimer': reqTimer,
                'medical_request_active': 'active',
            }
            return render(request, 'portalapp/patient/medical_request_details.html', context)

        else:
            return redirect(patientMedicalRequest)

    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)


@login_required(login_url='patientLogin')
def patientRequestDetails(request, pk):
    if request.user.is_authenticated and request.user.userType =='Patient':
        patientUser =  Patient.objects.get(user=request.user)

        if 'update_request' in request.POST:
            description = request.POST.get("description")
            
            if not (description) : 
                messages.warning(request, "Error , Field is required.")
                return redirect(patientRequestDetails) 
                
            else :
                # UPDATE DATA IN ILLNESS MODEL WHERE ID=PK
                update_request = Illness.objects.filter(id=pk,patient=patientUser).update(
                    description=description,
                )
                if update_request:
                    messages.success(request, "Treatment request updated successfully.")
                    # GET DOCTOR DETAILS FROM DOCTOR MODEL
                    patientRequest = Illness.objects.get(patient=patientUser, id=pk)
                    
                    context = {
                        'title': 'Patient Doctor Details',
                        'request': patientRequest,
                        'medical_request_active': 'active',
                    }
                    return render(request, 'portalapp/patient/edit_medical_request.html', context)


        elif 'delete_request' in request.POST:
            # DELETE FROM ILLNESS MODEL WHERE ID=PK
            delete_request = Illness.objects.get(id=pk)
            delete_request.delete()
            
            messages.success(request, "Treatment request deleted successfully.")
            return redirect(patientMedicalRequest)
        
        else: 
            if Illness.objects.filter(patient=patientUser, id=pk).exists() :
                # GET DOCTOR DETAILS FROM DOCTOR MODEL
                patientRequest = Illness.objects.get(patient=patientUser, id=pk)
                
                context = {
                    'title': 'Patient Doctor Details',
                    'request': patientRequest,
                    'medical_request_active': 'active',
                }
                return render(request, 'portalapp/patient/edit_medical_request.html', context)

            else:
                return redirect(patientMedicalRequest)
        
    else:
        messages.warning(request, ('You must login first!'))
        return redirect(patientLogin)
