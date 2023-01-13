from django.db import models
from users.models import User
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Speciality(models.Model):
    speciality_name = models.CharField(verbose_name='Speciality name', max_length=100, unique=True)
    description = models.TextField(verbose_name='Description')
    
    def __str__(self):
       return self.speciality_name


class Patient(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "SELECT GENDER"
        MALE = "MALE", "MALE"
        FEMALE = "FEMALE", "FEMALE" 

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    gender = models.CharField(verbose_name='Gender', max_length=10, choices=Gender.choices, default=Gender.SELECT)
    birthdate = models.DateField(verbose_name='Birthdate')
    phone = PhoneNumberField(region="", verbose_name='Phone number', unique=True)
    address = models.CharField(verbose_name='Location address', max_length=150)
    reg_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name,)


class Illness(models.Model):
    class Status(models.TextChoices):
        SELECT = "", "SELECT TO UPDATE STATUS"
        RESPONDED = "Responded", "RESPONDED"
        WAITING = "Waiting", "WAITING" 

    patient  = models.ForeignKey(Patient, verbose_name="Patient", on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Description')
    status = models.CharField(verbose_name='Request status', max_length=10, choices=Status.choices, default=Status.SELECT)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.patient.user.first_name, self.patient.user.last_name,)


class Doctor(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "SELECT GENDER"
        MALE = "MALE", "MALE"
        FEMALE = "FEMALE", "FEMALE" 

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    employ_id = models.CharField(verbose_name='Employ ID Code', max_length=100, unique=True)
    phone = PhoneNumberField(region="", verbose_name='Phone number', unique=True)
    gender = models.CharField(verbose_name='Gender', max_length=10, choices=Gender.choices, default=Gender.SELECT)
    doc_image = models.ImageField(upload_to='doctors/')
    reg_date = models.DateField(auto_now_add=True)

    def  image(self):
        return mark_safe('<img src="/../../../media/%s" width="70" />' % (self.doc_image))

    image.allow_tags = True 
    
    def __str__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.employ_id)


class TreatmentSuggestion(models.Model):
    illness  = models.ForeignKey(Illness, verbose_name="Patient's illness", on_delete=models.CASCADE)
    doctor  = models.ForeignKey(Doctor, verbose_name="Doctor to submit suggestion", on_delete=models.CASCADE)
    suggestion = models.CharField(verbose_name='Suggestion', max_length=100, unique=True)
    suggestionDescription = models.TextField(verbose_name='Suggestion description')
    sugg_dated = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.doctor, self.suggestion,)


class Treatment(models.Model):
    illness  = models.OneToOneField(Illness, verbose_name="Illness", on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Treatment description')
    date_confirmed = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.illness, self.description)


class requestTimer(models.Model):
    request = models.OneToOneField(Illness, verbose_name="Treatment request", on_delete=models.CASCADE)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()

    def __str__(self):
        return "{} - {}".format(self.start_period, self.end_period)
    


