from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.custom_login, name='account_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('receptionist_dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('user_deactivate/<int:pk>/', views.user_deactivate, name='user_deactivate'),
    path('user_activate/<int:pk>/', views.user_activate, name='user_activate'),
    path('create_admin_user/', views.create_admin_user, name='create_admin_user'),
    path('logout/', views.logout_view, name='logout'),
]
