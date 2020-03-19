import mimetypes
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .models import Operation, PatientConsent
from .forms import ConsentForm, OperationForm, SignatureForm
from portal.decorators import institution_required


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
def new_form(request):
    if request.method == 'POST':
        form = ConsentForm(request.POST, request.FILES)
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
        form = ConsentForm(initial=initial)
    return render(request, 'consent/new_consent.html', {'form': form})


@login_required
def view_form(request, form_id):
    consent = get_object_or_404(PatientConsent, pk=form_id)
    if consent.patient_signature is None or consent.patient_signature == "":
        patient_sig_type = ""
    else:
        patient_sig_type = mimetypes.MimeTypes().guess_type(consent.patient_signature.path)[0]
    
    if consent.physician_signature is None or consent.physician_signature == "":
        physician_sig_type = ""
    else:
        physician_sig_type = mimetypes.MimeTypes().guess_type(consent.physician_signature.path)[0]
    
    if consent.witness_signature is None or consent.witness_signature == "":
        witness_sig_type = ""
    else:
        witness_sig_type = mimetypes.MimeTypes().guess_type(consent.witness_signature.path)[0]

    return render(request, 'consent/view_consent.html', {"consent": consent, "patient": patient_sig_type, "physician": physician_sig_type, "witness": witness_sig_type})


@login_required
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
    
    if signature is None or signature == "":
        if request.method == 'POST':
            form = SignatureForm(request.POST, request.FILES)
            if form.is_valid():
                if signature_type == "patient":
                    consent.patient_signature = request.FILES['signature']
                elif signature_type == "physician":
                    consent.physician_signature = request.FILES['signature']
                    consent.consenting_physician = request.user
                elif signature_type == "witness":
                    consent.witness_signature = request.FILES['signature']
                    consent.witness_name = request.user
                consent.save()
                return redirect(f"/consent/patient_form/{form_id}")
            else:
                # display error
                pass
        else:
            form = SignatureForm()
        
        return render(request, "consent/new_signature.html", {"form": form, "consent": consent, "signature_type": signature_type})
    else:

        return redirect(f"/consent/patient_form/{form_id}")


@login_required
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
    # return redirect("/consent/")
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
