from django.contrib import admin
from babies.models import Baby


@admin.register(Baby)
class BabyAdmin(admin.ModelAdmin):
    """
    Admin para gestionar bebés en el panel de administración.
    """

    list_display = (
        "nombre",
        "sexo",
        "fecha_nacimiento",
        "parent",
        "peso",
        "created_at",
    )
    list_filter = ("sexo", "fecha_nacimiento", "created_at")
    search_fields = ("nombre", "parent__nombres", "parent__apellido_paterno")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Información básica",
            {"fields": ("parent", "nombre", "fecha_nacimiento", "sexo")},
        ),
        ("Información adicional", {"fields": ("peso", "alergias", "condiciones_salud")}),
        ("Metadatos", {"fields": ("created_at", "updated_at")}),
    )

