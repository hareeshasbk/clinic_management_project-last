from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
    path('appointment/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]

