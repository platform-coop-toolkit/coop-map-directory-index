from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import User
from mdi.models import Organization
from formtools.wizard.views import SessionWizardView
from .forms import BranchForm, RoleForm, BasicInfoForm, DetailedInfoForm, ContactInfoForm


# Profile flow
# This trivially branches to either the Organization or Individual Profile `django-formtools` wizard.
def profile(request):
    print(request.POST)
    if request.method == 'POST':
        if request.POST['type'] == 'org':
            return redirect('organization-profile')
        else:
            return redirect('individual-profile')

    else:
        profile_type_form = BranchForm()
        return render(request, 'maps/profiles/branch.html', {
            'profile_type_form': profile_type_form,
            'title': 'Organisation or Individual?'
        })


# This operates the Individual Profile wizard via `django-formtools`.
INDIVIDUAL_FORMS = [
    ('role', RoleForm),
    ('basic_info', BasicInfoForm),
    ('detailed_info', DetailedInfoForm),
    ('contact_info', ContactInfoForm)
]

INDIVIDUAL_TEMPLATES = {
    'role': 'maps/profiles/individual/role.html',
    'basic_info': 'maps/profiles/individual/basic_info.html',
    'detailed_info': 'maps/profiles/individual/detailed_info.html',
    'contact_info': 'maps/profiles/individual/contact_info.html',
}


class IndividualProfileWizard(SessionWizardView):
    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return render(self.request, 'maps/profiles/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


def index(request):
    template = loader.get_template('maps/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# Organization
def organization_detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    context = {
    }
    return render(request, 'maps/organization_detail.html', {'organization': organization})


# Individual
def individual_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
    }
    return render(request, 'maps/individual_detail.html', {'individual': user})


# Static pages
class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"


