from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from . import views


urlpatterns = [
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
