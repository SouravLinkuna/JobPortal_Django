from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin




# Method Name UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# Create 'UserDetails' models here
class UserDetails(AbstractBaseUser):
    email = models.EmailField(unique=True, error_messages={'email': ['Enter a valid email']})
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    mobile_number = models.IntegerField(unique=True, null=True, error_messages={'mobile_number': ['Enter a valid number']})
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    course = models.CharField(max_length=255, null=True)
    specialization = models.CharField(max_length=255, null=True)
    course_type = models.CharField(max_length=100, null=True)
    college = models.CharField(max_length=255, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    year_of_passing = models.IntegerField(null=True)
    skills = models.CharField(max_length=255, null=True)
    summary = models.TextField()
    experience_level = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=255)
    responsibilities = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
    worked_from = models.DateField(null=True)
    to = models.DateField(null=True)
    about_company = models.TextField()
    website = models.URLField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name', 'date_of_birth', 'gender', 'mobile_number', 'address', 'course', 'specialization', 'course_type', 'college', 'percentage', 'year_of_passing', 'skills', 'summary', 'experience_level', 'designation', 'responsibilities', 'company', 'location', 'worked_from', 'to', 'about_company', 'website']