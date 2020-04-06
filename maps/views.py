from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from accounts.models import Role
from mdi.models import Organization, SocialNetwork
from formtools.wizard.views import SessionWizardView
from .forms import BranchForm, RoleForm, BasicInfoForm, DetailedInfoForm, ContactInfoForm, UserSocialNetworkForm, UserSocialNetworkFormSet
from dal import autocomplete


# Inline Formset for SocialNetworks.
def manage_socialnetworks(request, user_id):
    user = get_user_model().objects.get(pk=user_id)
    SocialNetworkInlineFormSet = inlineformset_factory(get_user_model, SocialNetwork, fields=('title',))
    if request.method == "POST":
        formset = SocialNetworkInlineFormSet(request.POST, request.FILES, instance=user)
        if formset.is_valid():
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        formset = SocialNetworkInlineFormSet(instance=user)
    return render(request, 'manage_books.html', {'formset': formset})


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
    ('contact_info', ContactInfoForm),
    ('social_networks', UserSocialNetworkFormSet),
]

INDIVIDUAL_TEMPLATES = {
    'role': 'maps/profiles/individual/role.html',
    'basic_info': 'maps/profiles/individual/basic_info.html',
    'detailed_info': 'maps/profiles/individual/detailed_info.html',
    'contact_info': 'maps/profiles/individual/contact_info.html',
    'social_networks': 'maps/profiles/individual/social_networks.html',
}


class IndividualProfileWizard(SessionWizardView):
    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'detailed_info':
            role = self.get_cleaned_data_for_step('role')
            print('role.cleaned {}'.format(role))
            # Display `Services` if Individual is in Roles other than `Coop Founder` or `Coop Member`.
            for r in role['name']:
                if r.name not in ['Coop Founder', 'Coop Member']:
                    context.update({'display_services': True})
                if r.name == 'Service Provider':
                    context.update({'display_coops_worked_with': True})
                if r.name == 'Researcher':
                    context.update({
                        'display_field_of_study': True,
                        'display_affiliation': True,
                        'display_projects': True
                    })
        return context

    def done(self, form_list, **kwargs):
        return render(self.request, 'maps/profiles/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


# Autocomplete views for profile creation.
class OrganizationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Organization.objects.none()

        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


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
    user = get_object_or_404(settings.AUTH_USER_MODEL, pk=user_id)
    context = {
    }
    return render(request, 'maps/individual_detail.html', {'individual': user})


# Static pages
class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"


