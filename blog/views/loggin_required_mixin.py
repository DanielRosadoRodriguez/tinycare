from django.shortcuts import redirect
class LogginRequiredMixin:
    """Mixin to ensure the user is logged in."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:register')
        return super().dispatch(request, *args, **kwargs)