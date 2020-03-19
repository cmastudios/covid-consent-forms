import ipaddress
import os

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from portal.models import Institution, InstitutionNetwork
from .forms import InstitutionForm
import requests


def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, "portal/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


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
                    messages.error(request, f"You do not appear to be connected from {institution.name} (saw {clientip})")
            else:
                messages.error(request, "ReCAPTCHA failed.")
        else:
            messages.error(request, "Invalid institution")
    else:
        form = InstitutionForm()

    return render(request, "portal/select_institution.html", {"form": form})


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