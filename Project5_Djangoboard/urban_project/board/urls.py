from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('edit/', views.advertisement_list_to_edit, name='advertisement_list_to_edit'),
    path('edit/advertisement/<int:pk>/', views.advertisement_detail_edit, name='advertisement_detail_edit'),
    path('delete/', views.advertisement_list_to_delete, name='advertisement_list_to_delete'),
    path('delete/advertisement/<int:pk>/', views.advertisement_detail_delete, name='advertisement_detail_delete'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)