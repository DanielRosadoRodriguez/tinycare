
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..models.vaccine import Vaccine
from accounts.permissions.owner_permission_mixin import OwnerPermissionMixin
class VaccineListView(ListView):
    model = Vaccine
    template_name = 'vaccine_index.html'
    context_object_name = 'vaccines'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Todas las vacunas, para el calendario completo (sin paginación)
        context['all_vaccines'] = Vaccine.objects.all().order_by('applied_at')
        return context

class VaccineDetailView(OwnerPermissionMixin, ListView):
    permission_required = 'vaccines.view_vaccine'
    model = Vaccine
    template_name = 'vaccine_detail.html'
    context_object_name = 'vaccine'
    
class VaccineCreateView(CreateView):
    model = Vaccine
    template_name = 'vaccine_form.html'
    fields = ['name', 'applied_at', 'status']
    success_url = '/vaccines/'
    
class VaccineUpdateView(OwnerPermissionMixin, UpdateView):
    permission_required = 'vaccines.change_vaccine'
    model = Vaccine
    template_name = 'vaccine_form.html'
    fields = ['name', 'applied_at', 'status']
    success_url = '/vaccines/'

class VaccineDeleteView(OwnerPermissionMixin, DeleteView):
    permission_required = 'vaccines.delete_vaccine'
    model = Vaccine
    template_name = 'vaccine_confirm_delete.html'
    success_url = '/vaccines/'