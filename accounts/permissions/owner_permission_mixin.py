from django.contrib.auth.mixins import PermissionRequiredMixin

class OwnerPermissionMixin(PermissionRequiredMixin):
    """Restringe el acceso solo al propietario del objeto."""
    
    def has_permission(self):
        obj = self.get_object()
        return obj.author == self.request.user
