from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token

class CustomUserManager(BaseUserManager):
    def create_user(self, fullname, email, mobile_number, dob, profile=None, career_path=None, high_light=None, focus=None, years_of_experience=None, department=None, schedule=None, password=None, is_doctor=False, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be provided')
        if not fullname:
            raise ValueError('Full Name must be provided')
        if not mobile_number:
            raise ValueError('Mobile Number must be provided')
        if not dob:
            raise ValueError('Date of Birth must be provided')

        email = self.normalize_email(email)
        user = self.model(
            fullname=fullname,
            email=email,
            mobile_number=mobile_number,
            dob=dob,
            profile=profile,
            career_path=career_path,
            high_light=high_light,
            focus=focus,
            years_of_experience=years_of_experience,
            department=department,
            schedule=schedule,
            is_doctor=is_doctor,
            **extra_fields
        )

        if is_doctor:
            if not profile:
                raise ValueError('Profile must be provided for doctors')
            if not career_path:
                raise ValueError('Career Path must be provided for doctors')
            if not high_light:
                raise ValueError('Highlight must be provided for doctors')
            if not focus:
                raise ValueError('Focus must be provided for doctors')
            if years_of_experience is None:
                raise ValueError('Years of Experience must be provided for doctors')
            if not department:
                raise ValueError('Department must be provided for doctors')
            if not schedule:
                raise ValueError('Schedule must be provided for doctors')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_doctors(self, fullname, email, mobile_number, dob, profile, career_path, high_light, focus, years_of_experience, department, schedule, password=None):
        """
        Create and return a doctor with additional fields.
        """
        return self.create_user(
            fullname=fullname,
            email=email,
            mobile_number=mobile_number,
            dob=dob,
            profile=profile,
            career_path=career_path,
            high_light=high_light,
            focus=focus,
            years_of_experience=years_of_experience,
            department=department,
            schedule=schedule,
            password=password,
            is_doctor=True
        )

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    dob = models.DateField()

    # Doctor-specific fields
    profile = models.TextField(null=True, blank=True)
    career_path = models.CharField(max_length=255, null=True, blank=True)
    high_light = models.CharField(max_length=255, null=True, blank=True)
    focus = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    schedule = models.CharField(max_length=255, null=True, blank=True)

    # Status fields
    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'mobile_number', 'dob']

    def __str__(self):
        return self.fullname

class CustomToken(Token):
    user = models.ForeignKey(
        CustomUser,
        related_name='auth_tokens',
        on_delete=models.CASCADE
    )