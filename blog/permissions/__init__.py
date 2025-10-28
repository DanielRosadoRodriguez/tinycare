from django.contrib.auth.mixins import PermissionRequiredMixin

class OwnerPermissionMixin(PermissionRequiredMixin):
    
    def has_permission(self):
        obj = self.get_object()
        return obj.author == self.request.user
