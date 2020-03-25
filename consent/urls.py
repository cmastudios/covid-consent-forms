from django.urls import path
from . import views

from .views import landing

urlpatterns = [
    path('', landing, name='index'),
    path('operation/create/', views.new_operation, name='new_operation'),
    path('operation/<int:operation_id>/', views.view_operation, name='view_operation'),
    path('operation/<int:operation_id>/delete/', views.delete_operation, name='delete_operation'),
    path('<str:inst_id>/create/', views.new_form, name='new_consent_form'),
    path('<str:inst_id>/<int:form_id>/', views.view_form, name='view_consent_form'),
    path('<str:inst_id>/<int:form_id>/edit/', views.edit_form, name='edit_consent_form'),
    path('<str:inst_id>/<int:form_id>/signature/<str:signature_type>/', views.view_signature, name='view_signature'),
]
