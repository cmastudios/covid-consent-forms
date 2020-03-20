from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('verify/<str:token>/', views.verification_view, name='verification'),
    path('select_institution/', views.select_institution, name='select_institution'),
    path('deselect_institution/', views.deselect_institution, name='deselect_institution'),
]
