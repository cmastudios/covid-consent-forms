from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from . import views

from .views import landing

urlpatterns = [
    path('', landing, name='index'),
    path('operation/create/', views.new_operation, name='new_operation'),
    path('operation/<int:operation_id>/', views.view_operation, name='view_operation'),
    path('operation/<int:operation_id>/template.pdf', views.view_operation_template, name='view_operation_template'),
    path('operation/<int:operation_id>/delete/', views.delete_operation, name='delete_operation'),
    path('patient_form/create/', views.new_form, name='new_consent_form'),
    path('patient_form/<int:form_id>/', views.view_form, name='view_consent_form'),
    path('patient_form/<int:form_id>/signature/<str:signature_type>/', views.view_signature, name='view_signature'),
    path('patient_form/<int:form_id>/signature/<str:signature_type>/file', views.view_signature_file, name='view_signature_file'),
]