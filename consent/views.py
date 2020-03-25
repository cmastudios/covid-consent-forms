from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.middleware.csrf import rotate_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from .models import Operation, PatientConsent
from .forms import ConsentForm, OperationForm, SignatureForm, ConsentFormAuthorization

from portal.models import Institution, InstitutionEmail


def set_authorized_to_view_form(request, form_id):
    if "consent.forms_authorized" in request.session:
        request.session['consent.forms_authorized'].append(form_id)
    else:
        request.session['consent.forms_authorized'] = [form_id]
    request.session.modified = True


def check_authorized_to_view_form(request, form_id):
    if "consent.forms_authorized" in request.session:
        return form_id in request.session['consent.forms_authorized']
    else:
        return False


def get_user_institution(request):
    email = request.user.email
    for iemail in InstitutionEmail.objects.all():
        if email.endswith(iemail.email_suffix):
            return iemail.institution
    return None


@login_required
def landing(request):
    operations = Operation.objects.all()
    last_48h = timezone.now() - timedelta(hours=48)
    consent_forms = PatientConsent.objects.filter(creator=request.user, today_date__gte=last_48h)
    user_institution = get_user_institution(request)
    return render(request, "consent/landing_signedin.html", {
        "operations": operations, "consent_forms": consent_forms, "institution": user_institution
    })


@login_required
@permission_required("consent.add_patientconsent")
def new_form(request, inst_id):
    institution = get_object_or_404(Institution, identifier=inst_id)
    if request.method == 'POST':
        form = ConsentForm(request.POST, request.FILES)
        if form.is_valid():
            # save new operation
            consent = form.save(commit=False)
            password = User.objects.make_random_password(16)
            consent.institution = institution
            consent.creator = request.user
            consent.password_hash = make_password(password)
            consent.save()
            set_authorized_to_view_form(request, consent.id)
            # prevent resubmission
            rotate_token(request)
            response = render(request, 'consent/new_consent_created.html', {'id': consent.id, 'password': password, 'inst_id': inst_id})
            # 172800 seconds = 48.0 hours
            response.set_cookie(key=f"consent_id_{consent.id}_password", value=password, max_age=172800)
            return response
    else:
        form = ConsentForm(initial={'consenting_physician': f'{request.user.first_name} {request.user.last_name}'})
    return render(request, 'consent/new_consent.html', {'form': form})


def view_form(request, inst_id, form_id):
    consent = get_object_or_404(PatientConsent, pk=form_id)

    def display_prompt():
        return render(request, 'consent/check_consent_auth.html', {"form": form})

    def display_form():
        password = request.COOKIES.get(f"consent_id_{consent.id}_password")
        return render(request, 'consent/view_consent.html', {"consent": consent, "password": password, "inst_id": inst_id})

    if request.method == 'POST':
        # user is trying to submit password
        form = ConsentFormAuthorization(request.POST, instance=consent)
        if form.is_valid():
            # correct password
            set_authorized_to_view_form(request, form_id)
            return display_form()
        else:
            # incorrect password
            return display_prompt()

    elif check_authorized_to_view_form(request, form_id):
        # user has already successfully entered password
        return display_form()

    else:
        # user is not yet authorized
        form = ConsentFormAuthorization()
        return display_prompt()


@login_required
@permission_required("consent.change_patientconsent")
def edit_form(request, inst_id, form_id):
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


def view_signature(request, inst_id, form_id, signature_type):
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
                elif signature_type == "witness":
                    consent.witness_signature = request.FILES['signature']
                consent.save()
                return redirect("view_consent_form", inst_id=inst_id, form_id=form_id)
        else:
            form = SignatureForm()

        return render(request, "consent/new_signature.html",
                      {"form": form, "consent": consent, "signature_type": signature_type})
    else:
        return redirect("view_consent_form", inst_id=inst_id, form_id=form_id)


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
@permission_required("consent.delete_operation")
def delete_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    operation.delete()
    return redirect("index")
