from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class Appointment(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        # validators=[
        #     FileExtensionValidator(
        #         allowed_extensions=['pdf']
        #     )
        # ]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    appointment_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):

        super().clean()

        if self.appointment_date is None:
            return

        # Nouveau rendez-vous
        if self.pk is None:
            if self.appointment_date <= timezone.now():
                raise ValidationError({
                    'appointment_date':
                    "La date du rendez-vous doit être future."
                })

        # Rendez-vous existant
        else:
            old = Appointment.objects.filter(pk=self.pk).first()

            if old and old.appointment_date != self.appointment_date:
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date':
                        "La nouvelle date doit être future."
                    })

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]

        ordering = ['appointment_date']

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.appointment_date}"