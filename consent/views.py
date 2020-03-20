import mimetypes
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Operation, PatientConsent
from .forms import ConsentForm, OperationForm, SignatureForm


@login_required
def landing(request):
    operations = Operation.objects.all()
    is_phy = Q(consenting_physician=request.user)
    is_wit = Q(witness_name=request.user)
    phy_unsigned = Q(physician_signature__isnull=True) | Q(physician_signature__exact='')
    wit_unsigned = Q(witness_signature__isnull=True) | Q(witness_signature__exact='')
    waiting = PatientConsent.objects.filter((is_phy & phy_unsigned) | (is_wit & wit_unsigned))
    signed = PatientConsent.objects.filter((is_phy & ~phy_unsigned) | (is_wit & ~wit_unsigned))
    return render(request, "consent/landing_signedin.html", {
        "operations": operations, "waiting": waiting, "signed": signed
    })


@login_required
@permission_required("consent.add_patientconsent")
def new_form(request):
    if request.method == 'POST':
        form = ConsentForm(request.POST, request.FILES)
        if form.is_valid():
            # save new operation
            consent = form.save()
            return redirect("view_consent_form", form_id=consent.id)
    else:
        form = ConsentForm()
    return render(request, 'consent/new_consent.html', {'form': form})


@login_required
@permission_required("consent.view_patientconsent")
def view_form(request, form_id):
    consent = get_object_or_404(PatientConsent, pk=form_id)

    return render(request, 'consent/view_consent.html', {"consent": consent})


@login_required
@permission_required("consent.change_patientconsent")
def edit_form(request, form_id):
    consent: PatientConsent = get_object_or_404(PatientConsent, pk=form_id)
    if consent.has_any_signature:  # form is final
        return redirect("view_consent_form", form_id=form_id)

    if request.method == 'POST':
        form = ConsentForm(request.POST, request.FILES, instance=consent)
        if form.is_valid():
            # save new operation
            consent = form.save()
            return redirect("view_consent_form", form_id=consent.id)
    else:
        form = ConsentForm(instance=consent)
    return render(request, 'consent/new_consent.html', {'form': form})


@login_required
@permission_required("consent.view_patientconsent")
def view_signature(request, form_id, signature_type):
    consent = get_object_or_404(PatientConsent, pk=form_id)
    if signature_type == "patient":
        signature = consent.patient_signature
    elif signature_type == "physician":
        signature = consent.physician_signature
    elif signature_type == "witness":
        signature = consent.witness_signature
    else:
        raise Exception("Invalid signature type")

    # prevent overwriting old signature
    if signature is None or signature == "":
        if request.method == 'POST':
            form = SignatureForm(request.POST, request.FILES)
            if form.is_valid():
                # add signature, report user name
                if signature_type == "patient":
                    consent.patient_signature = request.FILES['signature']
                elif signature_type == "physician":
                    consent.physician_signature = request.FILES['signature']
                    consent.consenting_physician = request.user
                elif signature_type == "witness":
                    consent.witness_signature = request.FILES['signature']
                    consent.witness_name = request.user
                consent.save()
                return redirect("view_consent_form", form_id=form_id)
        else:
            form = SignatureForm()

        return render(request, "consent/new_signature.html",
                      {"form": form, "consent": consent, "signature_type": signature_type})
    else:
        return redirect("view_consent_form", form_id=form_id)


@login_required
@permission_required("consent.view_patientconsent")
def view_signature_file(request, form_id, signature_type):
    consent = get_object_or_404(PatientConsent, pk=form_id)
    if signature_type == "patient":
        signature = consent.patient_signature
    elif signature_type == "physician":
        signature = consent.physician_signature
    elif signature_type == "witness":
        signature = consent.witness_signature
    else:
        raise Exception("Invalid signature type")

    return FileResponse(open(signature.path, "rb"))


@login_required
@permission_required("consent.add_operation")
def new_operation(request):
    if request.method == 'POST':
        form = OperationForm(request.POST, request.FILES)
        if form.is_valid():
            # save new operation
            form.save()
            return redirect("index")
    else:
        form = OperationForm()

    return render(request, 'consent/new_operation.html', {"form": form})


@login_required
@permission_required("consent.view_operation")
def view_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    return render(request, "consent/view_operation.html", {"operation": operation})


@login_required
@permission_required("consent.view_operation")
def view_operation_template(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    path = operation.consent_form.path
    return FileResponse(open(path, "rb"))


@login_required
@permission_required("consent.delete_operation")
def delete_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    operation.delete()
    return redirect("index")
