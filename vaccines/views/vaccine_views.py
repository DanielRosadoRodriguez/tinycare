
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from ..models.vaccine import Vaccine
from accounts.models.profile_parent import ProfileParent
from accounts.permissions.owner_permission_mixin import OwnerPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from babies.models.baby_model import Baby

class VaccineListView(ListView, LoginRequiredMixin):
    model = Vaccine
    template_name = 'vaccine_index.html'
    context_object_name = 'vaccines'
    
    def get_queryset(self):
        """Retorna solo las vacunas de los bebés del padre actual."""
        parent = ProfileParent.objects.get(user=self.request.user)
        return Vaccine.objects.filter(baby__parent=parent).order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = ProfileParent.objects.get(user=self.request.user)
        context['all_vaccines'] = self.get_queryset()
        return context

class VaccineDetailView(DetailView, OwnerPermissionMixin, LoginRequiredMixin):
    permission_required = 'vaccines.view_vaccine'
    model = Vaccine
    template_name = 'vaccine_detail.html'
    context_object_name = 'vaccine'
    
class VaccineCreateView(CreateView, LoginRequiredMixin):
    model = Vaccine
    template_name = 'vaccine_form.html'
    fields = ['name', 'applied_at', 'status']
    success_url = '/vaccines/'
    def form_valid(self, form):
        baby_id = self.kwargs.get('id_baby') or self.request.POST.get('baby')
        if baby_id:
            form.instance.baby = Baby.objects.get(pk=baby_id)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_baby = self.kwargs.get('id_baby', None)
        if not pk_baby:
            context['babies'] = Baby.objects.all().filter(parent__user=self.request.user)
        return context
    
class VaccineUpdateView(UpdateView, OwnerPermissionMixin, LoginRequiredMixin):
    permission_required = 'vaccines.change_vaccine'
    model = Vaccine
    template_name = 'vaccine_form.html'
    fields = ['name', 'applied_at', 'status']
    success_url = '/vaccines/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_baby = self.kwargs.get('id_baby', None)
        if not pk_baby:
            context['babies'] = Baby.objects.all().filter(parent__user=self.request.user)
        return context

class VaccineDeleteView(DeleteView, OwnerPermissionMixin, LoginRequiredMixin):
    permission_required = 'vaccines.delete_vaccine'
    model = Vaccine
    template_name = 'vaccine_confirm_delete.html'
    success_url = '/vaccines/'