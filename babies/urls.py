"""
URLs para la app babies.
"""

from django.urls import path
from babies.views import (
    BabyListView,
    BabyDetailView,
    BabyCreateView,
    BabyUpdateView,
    BabyDeleteView,
)

app_name = "babies"

urlpatterns = [
    path("", BabyListView.as_view(), name="baby_list"),
    path("nuevo/", BabyCreateView.as_view(), name="baby_create"),
    path("<int:pk>/", BabyDetailView.as_view(), name="baby_detail"),
    path("<int:pk>/editar/", BabyUpdateView.as_view(), name="baby_update"),
    path("<int:pk>/eliminar/", BabyDeleteView.as_view(), name="baby_delete"),
]
