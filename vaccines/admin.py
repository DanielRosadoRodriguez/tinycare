from django.contrib import admin

# Register your models here.
from .models.vaccine import Vaccine
admin.site.register(Vaccine)