from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,max_length_validator
# Create your models here.
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass 
class Doctor(User):
    license_number = models.CharField(max_length=6,unique=True, validators=[MinLengthValidator(6)])
    phone_number = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialty = models.ManyToManyField('Specialty', related_name='doctors')
class Patient(User):
    national_id = models.CharField(max_length=8,unique=True, validators=[regex_validator(r'^\d{8}$', 'National ID must be exactly 8 digits.')])
    phone_number = models.CharField(max_length=8)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
             models.CheckConstraint(
                 fields=["doctor","appointment_date"],
                    name="doctor_appointment_date_check",
                    violation_error_message="A doctor cannot have more than one appointment at the same date and time."

             )
         ]
class Specialty(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def validate_past_date(value):
        if value >= timezone.localdate():
         raise ValidationError(
                "La date de naissance doit être antérieure à aujourd'hui."
            )

        