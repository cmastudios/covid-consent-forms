import ipaddress
import os
import smtplib
import hashlib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from portal.models import Institution, InstitutionNetwork, InstitutionEmail
from .forms import InstitutionForm, CreateUserForm
from covidconsent import settings
import requests


def logout_view(request):
    logout(request)
    return redirect("login")


def create_verification_token(username):
    m = hashlib.sha256()
    m.update(settings.SECRET_KEY.encode("utf-8"))
    m.update(username.encode("utf-8"))
    return m.hexdigest()


def check_verification_token(username, token):
    return create_verification_token(username) == token


def send_verification_email(username, email):
    m = create_verification_token(username)
    link = f"https://coviddemo.innovationdx.com/portal/verify/{m}/"
    send_mail(
        "Verify your email",
        f"In order to access SLU Health Patient Consent Portal, you must verify your institutional affiliation. "
        f"Use this link to verify your ownership of this email:\n"
        f"{link}\n\n"
        f"Thanks for using SLU Health Patient Consent Portal.\n"
        f"Not expecting this email? Someone may have used your email address by mistake. Please disregard this message.",
        "consentportal@innovationdx.com",
        [email],
        fail_silently=False,
    )


def signup_view(request):
    if request.method == 'POST':
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            email = forms.cleaned_data.get('email')
            raw_password = forms.cleaned_data.get('password1')
            send_verification_email(username, email)
            forms.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        return redirect('login')
    forml = AuthenticationForm()
    return render(request, 'portal/login.html', {'login': forml, 'signup': forms})


def login_view(request):
    if request.method == 'POST':
        forml = AuthenticationForm(data=request.POST)
        if forml.is_valid():
            user = forml.get_user()
            login(request, user)

            return redirect('index')
    else:
        forml = AuthenticationForm()
    forms = CreateUserForm()
    return render(request, 'portal/login.html', {'login': forml, 'signup': forms})


def password_reset_view(request):
    pass


@login_required
def verification_view(request, token):
    if check_verification_token(request.user.username, token):
        permission = Permission.objects.get(name='Can add patient consent')
        request.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view patient consent')
        request.user.user_permissions.add(permission)
        messages.success(request, "Your account has been successfully verified.")
        return redirect('index')
    else:
        messages.error(request, "Account verification was unsuccessful.")
        return redirect('index')




def select_institution(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():  # check valid institution
            institution = form.cleaned_data["institution"]
            clientip = get_client_ip(request)
            r = requests.post("https://www.google.com/recaptcha/api/siteverify",
                              {
                                  "secret": os.environ["RECAPTCHA_SECRET"],
                                  "response": request.POST["g-recaptcha-response"]
                              })
            if r.json()["success"]:  # check passed CAPTCHA
                if check_client_ip_in_institution_network(clientip, institution):
                    request.session["institution_id"] = institution.id
                    request.session["institution_name"] = institution.name
                    return redirect("index")
                else:
                    messages.error(request,
                                   f"You do not appear to be connected from {institution.name} (saw {clientip})")
            else:
                messages.error(request, "ReCAPTCHA failed.")
        else:
            messages.error(request, "Invalid institution")
    else:
        form = InstitutionForm()

    return render(request, "portal/select_institution.html", {"form": form})


def deselect_institution(request):
    del request.session["institution_id"]
    del request.session["institution_name"]
    return redirect("select_institution")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_client_ip_in_institution_network(clientip, institution):
    clientip = ipaddress.ip_address(clientip)
    networks = InstitutionNetwork.objects.filter(institution=institution)
    for network in networks:
        networkip = ipaddress.ip_network(network.ip)
        if clientip in networkip:
            return True
    return False


