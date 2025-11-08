from django.urls import path
from privacy.views import privacy_notice_view, actualizar_consentimientos_view, download_personal_data

app_name = "privacy"

urlpatterns = [
    path("", privacy_notice_view, name="notice"),
    path("consentimientos/", actualizar_consentimientos_view, name="actualizar_consentimientos"),
    path("descargar-datos/", download_personal_data, name="download_data"),
]
