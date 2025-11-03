from django.urls import path
import vaccines.views.vaccine_views as vaccine_views
app_name = "vaccines"

urlpatterns = [
    path("", vaccine_views.VaccineListView.as_view(), name="vaccines-index"),
    path("<int:pk>/", vaccine_views.VaccineDetailView.as_view(), name="vaccines-detail"),
    path("create/<int:id_baby>", vaccine_views.VaccineCreateView.as_view(), name='vaccines-create'),
    path("create/", vaccine_views.VaccineCreateView.as_view(), name='vaccines-create'),
    path("edit/<int:pk>", vaccine_views.VaccineUpdateView.as_view(), name="vaccines-edit"),
    path("delete/<int:pk>", vaccine_views.VaccineDeleteView.as_view(), name="vaccines-delete"),
]
