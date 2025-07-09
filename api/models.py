import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class Document(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_uploads')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    type = models.CharField(max_length=20, choices=(('report', 'Report'), ('prescription', 'Prescription')))
    timestamp = models.DateTimeField(auto_now_add=True)
    doc_uid = models.UUIDField(default=uuid.uuid4, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True) 
    
    def __str__(self):
        return f"{self.uploaded_by.username} -> {self.patient.username}: {self.file.name}"

