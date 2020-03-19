from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .models import Operation, PatientConsent
from .forms import ConsentForm, OperationForm


@login_required
def landing(request):
    operations = Operation.objects.all()
    if request.user.groups.filter(name='Doctor').exists():
        yours = PatientConsent.objects.filter(physician=request.user)
        waiting = yours.filter(physician_signature=False)
        signed = yours.filter(physician_signature=True)
    elif request.user.groups.filter(name='Nurse').exists():
        yours = PatientConsent.objects.filter(nurse=request.user)
        waiting = yours.filter(nurse_signature=False)
        signed = yours.filter(nurse_signature=True)
    else:
        waiting = signed = []
    return render(request, "consent/landing.html", {"operations": operations, "forms_awaiting_your_signature": waiting, "forms_signed_by_you": signed})


@login_required
def new_form(request):
    if request.method == 'POST':
        form = ConsentForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            # save new operation
            consent = form.save(commit=False)
            if consent.physician == request.user:
                consent.physician_signature = True
            if consent.nurse == request.user:
                consent.nurse_signature = True
            if consent.inability is not None and len(consent.inability) > 0:
                consent.consent_status = 3
            if (consent.relative_name is not None and len(consent.relative_name) > 0):
                consent.consent_status = 2
            consent.save()
            return redirect(f"/consent/patient_form/{consent.id}/")
        else:
            # display error
            pass
    else:
        initial = {}
        if request.user.groups.filter(name='Doctor').exists():
            initial["physician"] = request.user
        elif request.user.groups.filter(name='Nurse').exists():
            initial["nurse"] = request.user
        form = ConsentForm(request.user, initial=initial)
    return render(request, 'consent/new_consent.html', {'form': form})


@login_required
def view_form(request, form_id):
    consent = get_object_or_404(PatientConsent, pk=form_id)
    doctor = nurse = False
    if request.user.groups.filter(name='Doctor').exists():
        doctor = True
    elif request.user.groups.filter(name='Nurse').exists():
        nurse = True
    return render(request, 'consent/view_consent.html', {"consent": consent, "is_doctor": doctor, "is_nurse": nurse})


@login_required
def nurse_sign(request, form_id):
    if not request.user.groups.filter(name='Nurse').exists():
        raise Exception("You're not a nurse")
    consent = get_object_or_404(PatientConsent, pk=form_id)
    consent.nurse = request.user
    consent.nurse_signature = True
    consent.save()
    return render(request, 'consent/view_consent.html', {"consent": consent})


@login_required
def physician_sign(request, form_id):
    if not request.user.groups.filter(name='Doctor').exists():
        raise Exception("You're not a doctor")
    consent = get_object_or_404(PatientConsent, pk=form_id)
    consent.physician = request.user
    consent.physician_signature = True
    consent.save()
    return render(request, 'consent/view_consent.html', {"consent": consent})


@login_required
def view_consent_video(request, form_id):
    consent = get_object_or_404(PatientConsent, pk=form_id)
    path = consent.consent_video.path
    return FileResponse(open(path, "rb"))


@login_required
def new_operation(request):
    if request.method == 'POST':
        form = OperationForm(request.POST, request.FILES)
        if form.is_valid():
            # save new operation
            form.save()
            return redirect("/consent/")
        else:
            # display error
            pass
    else:
        form = OperationForm()
    return render(request, 'consent/new_operation.html', {"form": form})


@login_required
def view_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    return render(request, "consent/view_operation.html", {"operation": operation})


@login_required
def view_operation_template(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    path = operation.consent_form.path
    return FileResponse(open(path, "rb"))


@login_required
def delete_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    operation.delete()
    return redirect("/consent/")
