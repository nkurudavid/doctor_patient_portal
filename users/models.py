from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, userType, password=None):
        """
        Creates and saves a User with the given email, userType and password.
        """
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            userType=userType,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, email, userType, password=None):
        """
        Creates and saves a superuser with the given email, userType and password.
        """
        user = self.create_user( 
            first_name,
            last_name,
            email,
            password=password,
            userType=userType,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        SELECT = "", "SELECT USER TYPE"
        ADMIN = "Admin", "ADMIN"
        DEAN = "Doctor", "DOCTOR" 
        VOTER = "Patient", "PATIENT"
    
    first_name = models.CharField(verbose_name='First Name', max_length=100)
    last_name = models.CharField(verbose_name='Last Name', max_length=100)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    userType = models.CharField(verbose_name='User Type', max_length=50, choices=Types.choices, default=Types.SELECT)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','userType',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff_member(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff