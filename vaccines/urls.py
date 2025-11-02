from django.urls import path
import vaccines.views.vaccine_views as vaccine_views
app_name = "vaccines"

urlpatterns = [
    path("", vaccine_views.VaccineListView.as_view(), name="vaccine-index"),
    path("<int:pk>/", vaccine_views.VaccineDetailView.as_view(), name="vaccine-detail"),
    path("create/", vaccine_views.VaccineCreateView.as_view(), name="vaccine-create"),
    path("<int:pk>/edit/", vaccine_views.VaccineUpdateView.as_view(), name="vaccine-edit"),
    path("<int:pk>/delete/", vaccine_views.VaccineDeleteView.as_view(), name="vaccine-delete"),
]
