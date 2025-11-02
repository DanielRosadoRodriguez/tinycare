"""
Vistas CRUD para gestión de bebés.
Solo los padres pueden ver/editar/eliminar sus propios bebés.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.exceptions import PermissionDenied

from babies.models import Baby
from babies.forms import BabyForm
from babies.permissions import BabyOwnerPermissionMixin
from accounts.models.profile_parent import ProfileParent


class BabyListView(LoginRequiredMixin, ListView):
    """
    Lista todos los bebés del padre/madre autenticado.
    """

    model = Baby
    template_name = "babies/baby_list.html"
    context_object_name = "babies"
    paginate_by = 10

    def get_queryset(self):
        # Solo mostrar bebés del padre autenticado
        try:
            parent_profile = ProfileParent.objects.get(user=self.request.user)
            return Baby.objects.filter(parent=parent_profile).order_by(
                "-fecha_nacimiento"
            )
        except ProfileParent.DoesNotExist:
            return Baby.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar si el usuario tiene perfil de padre
        try:
            context["is_parent"] = ProfileParent.objects.filter(
                user=self.request.user
            ).exists()
        except Exception:
            context["is_parent"] = False
        return context


class BabyDetailView(LoginRequiredMixin, BabyOwnerPermissionMixin, DetailView):
    """
    Muestra el detalle de un bebé específico.
    Solo accesible por el padre/madre propietario.
    """

    model = Baby
    template_name = "babies/baby_detail.html"
    context_object_name = "baby"


class BabyCreateView(LoginRequiredMixin, CreateView):
    """
    Crea un nuevo registro de bebé.
    Solo accesible para usuarios con ProfileParent.
    """

    model = Baby
    form_class = BabyForm
    template_name = "babies/baby_form.html"
    success_url = reverse_lazy("babies:baby_list")

    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario tenga un perfil de padre
        try:
            ProfileParent.objects.get(user=request.user)
        except ProfileParent.DoesNotExist:
            raise PermissionDenied(
                "Solo los padres/madres pueden registrar bebés. "
                "Por favor, regístrate como padre/madre primero."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Asignar automáticamente el padre autenticado
        parent_profile = ProfileParent.objects.get(user=self.request.user)
        form.instance.parent = parent_profile
        messages.success(
            self.request, f"Bebé {form.instance.nombre} registrado correctamente."
        )
        return super().form_valid(form)


class BabyUpdateView(LoginRequiredMixin, BabyOwnerPermissionMixin, UpdateView):
    """
    Edita la información de un bebé existente.
    Solo accesible por el padre/madre propietario.
    """

    model = Baby
    form_class = BabyForm
    template_name = "babies/baby_form.html"
    success_url = reverse_lazy("babies:baby_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"Información de {form.instance.nombre} actualizada."
        )
        return super().form_valid(form)


class BabyDeleteView(LoginRequiredMixin, BabyOwnerPermissionMixin, DeleteView):
    """
    Elimina un registro de bebé.
    Solo accesible por el padre/madre propietario.
    """

    model = Baby
    template_name = "babies/baby_confirm_delete.html"
    success_url = reverse_lazy("babies:baby_list")

    def delete(self, request, *args, **kwargs):
        baby = self.get_object()
        messages.success(request, f"Registro de {baby.nombre} eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
