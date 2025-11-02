from django.db import models
# Create your models here.
class Vaccine(models.Model):
    APPLIED = 'AP'
    PENDING = 'PE'
    
    STATUS_CHOICES = [
        (APPLIED, 'Applied'),
        (PENDING, 'Pending'),
    ]
    
    name = models.CharField(max_length=100)
    applied_at = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)