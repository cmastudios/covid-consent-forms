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
    path('patient_form/<int:form_id>/nurse_sign/', views.nurse_sign, name='nurse_sign'),
    path('patient_form/<int:form_id>/physician_sign/', views.physician_sign, name='physician_sign'),
    path('patient_form/<int:form_id>/consent_video', views.view_consent_video, name='view_consent_video'),
]