from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

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