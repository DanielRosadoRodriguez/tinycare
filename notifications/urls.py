from django.urls import path
from notifications import views
# Esto es importante para que puedas usar {% url 'notifications:api-unread' %}
app_name = "notifications"

urlpatterns = [
    # Ruta para la lista de notificaciones (ej: /notifications/)
    path('', views.NotificationListView.as_view(), name='notification-list'),
    
    # Ruta para ver una notificación específica (ej: /notifications/5/)
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
]