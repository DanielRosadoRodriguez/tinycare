"""
Init file para privacy.views
"""
from privacy.views.base_views import privacy_notice_view, actualizar_consentimientos_view
from privacy.views.download_data import download_personal_data

__all__ = ['privacy_notice_view', 'actualizar_consentimientos_view', 'download_personal_data']
