from django.urls import path
from . import views


app_name = 'medications'  # Add this line

# 


urlpatterns = [
    # Medication URLs
    path('medications/', views.medication_list, name='medication_list'),
    path('medications/create/', views.medication_create, name='medication_create'),
    path('medications/edit/<int:pk>/', views.medication_edit, name='medication_edit'),
    path('medications/delete/<int:pk>/', views.medication_delete, name='medication_delete'),

    # Prescription URLs
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/create/', views.prescription_create, name='prescription_create'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
]


# urlpatterns = [
#     path('medication_list/', views.medication_list, name='medication_list'),
#     path('patient/<int:patient_id>/create_prescription/', views.create_prescription, name='create_prescription'),
#     path('patient_list/', views.patient_list, name='patient_list'),
#     path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
#     path('patient/<int:patient_id>/create_prescription/', views.create_prescription, name='create_prescription'),
#     path('patient/<int:patient_id>/create_prescription/success', views.create_prescription_success, name='create_prescription_success'),
# ]
