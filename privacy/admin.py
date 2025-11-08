from django.contrib import admin
from django import forms
from privacy.models import PrivacyNotice, PrivacyAcceptance


class PrivacyNoticeForm(forms.ModelForm):
    """
    Formulario personalizado para subir archivos .md
    """
    markdown_file = forms.FileField(
        label="Archivo Markdown (.md)",
        required=False,
        help_text="Arrastra y suelta un archivo .md aquí o haz clic para seleccionar",
        widget=forms.FileInput(attrs={
            'accept': '.md,text/markdown',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = PrivacyNotice
        fields = ['markdown_file']
    
    def clean_markdown_file(self):
        file = self.cleaned_data.get('markdown_file')
        if file:
            if not file.name.endswith('.md'):
                raise forms.ValidationError("Solo se permiten archivos .md")
        return file
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        markdown_file = self.cleaned_data.get('markdown_file')
        
        if markdown_file:
            # Leer contenido del archivo
            content = markdown_file.read().decode('utf-8')
            instance.content = content
        
        # Siempre activar el nuevo aviso
        instance.is_active = True
        
        if commit:
            instance.save()
        return instance


@admin.register(PrivacyNotice)
class PrivacyNoticeAdmin(admin.ModelAdmin):
    """
    Admin para gestionar avisos de privacidad.
    Solo superusuarios pueden crear/editar avisos.
    """
    form = PrivacyNoticeForm
    list_display = ("id", "created_at", "is_active", "content_hash_short", "uploaded_by")
    list_filter = ("is_active", "created_at")
    list_editable = ("is_active",)
    readonly_fields = ("content", "content_hash", "created_at", "uploaded_by")
    fields = ("markdown_file", "content", "content_hash", "uploaded_by", "created_at", "is_active")
    
    class Media:
        js = ('privacy/admin/privacy_notice.js',)
    
    def content_hash_short(self, obj):
        """Muestra los primeros 16 caracteres del hash."""
        return obj.content_hash[:16] + "..." if obj.content_hash else "-"
    content_hash_short.short_description = "Hash (corto)"
    
    def has_add_permission(self, request):
        """Solo superusuarios pueden agregar avisos."""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Solo se permite cambiar el estado is_active."""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """No se permite eliminar avisos."""
        return False
    
    def save_model(self, request, obj, form, change):
        """Asigna el usuario que sube el aviso."""
        if not change:  # Solo al crear
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PrivacyAcceptance)
class PrivacyAcceptanceAdmin(admin.ModelAdmin):
    """
    Admin para ver quién aceptó qué aviso.
    Solo lectura.
    """
    list_display = ("user", "privacy_notice", "accepted_at")
    list_filter = ("accepted_at", "privacy_notice")
    search_fields = ("user__email",)
    readonly_fields = ("user", "privacy_notice", "accepted_at")
    
    def has_add_permission(self, request):
        """No se pueden crear manualmente."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Solo lectura."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """No se pueden eliminar."""
        return False
