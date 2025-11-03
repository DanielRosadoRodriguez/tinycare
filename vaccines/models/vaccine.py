from django.db import models
from babies.models.baby_model import Baby  
class Vaccine(models.Model):
    APPLIED = 'AP'
    PENDING = 'PE'
    
    STATUS_CHOICES = [
        (APPLIED, 'Aplicada'), 
        (PENDING, 'Pendiente'),
    ]
    
    baby = models.ForeignKey(
        Baby,  
        on_delete=models.CASCADE,
        related_name='vaccines', # Nombre para acceder a las vacunas desde el objeto Baby (ej: baby.vaccines.all())
        verbose_name='Bebé asociado',
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=100, verbose_name="Nombre de la vacuna")
    # Nota: Si `applied_at` es la fecha de aplicación, es mejor que no sea obligatorio si el status es 'PENDING'
    applied_at = models.DateField(
        verbose_name="Fecha de aplicación"
    )
    status = models.CharField(
        max_length=2, 
        choices=STATUS_CHOICES, 
        default=PENDING,
        verbose_name="Estado"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Vacuna Registrada"
        verbose_name_plural = "Vacunas Registradas"
        
    def __str__(self):
        return f"{self.name} para {self.baby.nombre} ({self.get_status_display()})"