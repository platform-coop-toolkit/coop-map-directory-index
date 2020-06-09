from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from accounts.models import UserSocialNetwork
from mdi.models import Organization, SocialNetwork
from formtools.wizard.views import SessionWizardView
from .forms import IndividualRolesForm, IndividualBasicInfoForm, IndividualMoreAboutYouForm, IndividualDetailedInfoForm, IndividualContactInfoForm, IndividualSocialNetworkFormSet, OrganizationTypeForm, OrganizationBasicInfoForm, OrganizationContactInfoForm, OrganizationDetailedInfoForm
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
# This operates the Individual Profile wizard via `django-formtools`.
INDIVIDUAL_FORMS = [
    ('basic_info', IndividualBasicInfoForm),
    ('contact_info', IndividualContactInfoForm),
    ('roles', IndividualRolesForm),
    ('more_about_you', IndividualMoreAboutYouForm),
    ('detailed_info', IndividualDetailedInfoForm),
    ('social_networks', IndividualSocialNetworkFormSet),
]

INDIVIDUAL_TEMPLATES = {
    'basic_info': 'maps/profiles/individual/basic_info.html',
    'contact_info': 'maps/profiles/individual/contact_info.html',
    'roles': 'maps/profiles/individual/roles.html',
    'more_about_you': 'maps/profiles/individual/more_about_you.html',
    'detailed_info': 'maps/profiles/individual/detailed_info.html',
    'social_networks': 'maps/profiles/individual/social_networks.html',
}

ORGANIZATION_FORMS = [
    ('org_type', OrganizationTypeForm),
    ('basic_info', OrganizationBasicInfoForm),
    ('contact_info', OrganizationContactInfoForm),
    ('detailed_info', OrganizationDetailedInfoForm)
]    

ORGANIZATION_TEMPLATES = {
    'org_type': 'maps/profiles/organization/org_type.html',
    'basic_info': 'maps/profiles/organization/basic_info.html',
    'contact_info': 'maps/profiles/organization/contact_info.html',
    'detailed_info': 'maps/profiles/organization/detailed_info.html'
}

class IndividualProfileWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current in ['more_about_you', 'detailed_info']:
            roles = self.get_cleaned_data_for_step('roles')['roles']
            print('roles.cleaned {}'.format(roles))
            for r in roles:
                if r.name == 'Coop Member':
                    context.update({'display_member_of': True})
                if r.name == 'Coop Founder':
                    context.update({'display_founder_of': True})
                if r.name == 'Service Provider':
                    context.update({
                        'display_services': True,
                        'display_coops_worked_with': True
                    })
                if r.name == 'Researcher':
                    context.update({
                        'display_field_of_study': True,
                        'display_affiliation': True,
                        'display_projects': True
                    })
        return context

    # Attempt to solve SocialNetwork problem on profile pages.
    def get_form_initial(self, step):
        initial = []
        if step == 'social_networks':
            socialnetworks = SocialNetwork.objects.all()
            for index, sn in enumerate(socialnetworks):
                initial.append({
                    'socialnetwork' : sn,
                    'name': sn.name,
                    'hint' : sn.hint,
                })
            # print(initial)
        return self.initial_dict.get('social_networks', initial)

    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user
        form_dict = self.get_all_cleaned_data()
        for k, v in form_dict.items():
            if k not in ['roles', 'languages', 'services', 'challenges', 'formset-social_networks', ]:
                setattr(user, k, v)
        user.has_profile = True
        user.save()
        user.roles.set(form_dict['roles'])
        user.languages.set(form_dict['languages'])
        user.services.set(form_dict['services'])
        user.challenges.set(form_dict['challenges'])

        for sn in form_dict['formset-social_networks']:
            if sn['identifier'] != '':
                UserSocialNetwork.objects.create(user=user, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])

        return redirect('individual-detail', user_id=user.id)


# Autocomplete views for profile creation.
class OrganizationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Organization.objects.none()

        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class OrganizationProfileWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [ORGANIZATION_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        return context

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
    user = get_object_or_404(get_user_model(), pk=user_id)
    context = {
    }
    return render(request, 'maps/individual_detail.html', {'individual': user})


# Static pages
class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"

class AboutPageView(TemplateView):
    template_name = "maps/about.html"

