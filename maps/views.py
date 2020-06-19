from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from accounts.models import UserSocialNetwork
from mdi.models import Organization, SocialNetwork
from formtools.wizard.views import SessionWizardView
from .forms import IndividualProfileDeleteForm, RolesForm, BasicInfoForm, DetailedInfoForm, ContactInfoForm, UserSocialNetworkFormSet
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
    ('roles', RolesForm),
    ('basic_info', BasicInfoForm),
    ('detailed_info', DetailedInfoForm),
    ('contact_info', ContactInfoForm),
    ('social_networks', UserSocialNetworkFormSet),
]

INDIVIDUAL_TEMPLATES = {
    'roles': 'maps/profiles/individual/roles.html',
    'basic_info': 'maps/profiles/individual/basic_info.html',
    'detailed_info': 'maps/profiles/individual/detailed_info.html',
    'contact_info': 'maps/profiles/individual/contact_info.html',
    'social_networks': 'maps/profiles/individual/social_networks.html',
}


class IndividualProfileWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'detailed_info':
            roles = self.get_cleaned_data_for_step('roles')
            print('roles.cleaned {}'.format(roles))
            # Display `Services` if Individual is in Roles other than `Coop Founder` or `Coop Member`.
            for r in roles:
                if r not in ['Coop Founder', 'Coop Member']:
                    context.update({'display_services': True})
                if r == 'Service Provider':
                    context.update({'display_coops_worked_with': True})
                if r == 'Researcher':
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

class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('my-profiles')
    success_message = "You have successfully deleted the organizational profile for %(name)s."
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(OrganizationDelete, self).delete(request, *args, **kwargs)

# My Profiles
@login_required
def my_profiles(request):
    user = request.user
    user_orgs = Organization.objects.filter(admin_email=user.email)

    if request.method == 'POST':
        form = IndividualProfileDeleteForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully deleted your personal profile.')
            return HttpResponseRedirect('/my-profiles/')
    else:
        form = IndividualProfileDeleteForm(instance=user, initial={'has_profile': False})

    context = {
        'user_orgs': user_orgs,
        'form': form
    }

    return render(request, 'maps/my_profiles.html', context)

# Account Seetings
@login_required
def account_settings(request):
    return render(request, 'maps/account_settings.html')

# Static pages
class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"

class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"

class AboutPageView(TemplateView):
    template_name = "maps/about.html"

