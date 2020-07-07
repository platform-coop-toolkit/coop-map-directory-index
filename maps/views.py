from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory  # ModelMultipleChoiceField, SelectMultiple
from accounts.models import UserSocialNetwork
from mdi.models import Organization, SocialNetwork, OrganizationSocialNetwork, Relationship, EntitiesEntities, \
    Tool, Niche
from formtools.wizard.views import SessionWizardView
from .forms import GeolocationForm, IndividualProfileDeleteForm, IndividualRolesForm, IndividualBasicInfoForm, \
    IndividualMoreAboutYouForm, IndividualDetailedInfoForm, IndividualContactInfoForm, IndividualSocialNetworkFormSet, \
    IndividualEditSocialNetworkFormSet, IndividualOverviewUpdateForm, IndividualBasicInfoUpdateForm, \
    OrganizationTypeForm, OrganizationBasicInfoForm, OrganizationContactInfoForm, OrganizationDetailedInfoForm, \
    OrganizationScopeAndImpactForm, OrganizationSocialNetworkFormSet, OrganizationBasicInfoUpdateForm, \
    OrganizationOverviewUpdateForm, OrganizationContactUpdateForm, OrganizationEditSocialNetworkFormSet, \
    ToolBasicInfoForm, ToolDetailedInfoForm
from django_countries import countries
from django.contrib.gis.geos import Point
import os
import requests


def contact_info_to_lng_lat(contact_info):
    address_string = ''
    if contact_info['address'] != '':
        address_string += '{}, '.format(contact_info['address'])
    if contact_info['city'] != '':
        address_string += '{}, '.format(contact_info['city'])
    if contact_info['state'] != '':
        address_string += '{}, '.format(contact_info['state'])
    if contact_info['country'] != '':
        address_string += '{}, '.format(dict(countries)[contact_info['country']])
    if contact_info['postal_code'] != '':
        address_string += '{}, '.format(contact_info['postal_code'])
    address_string = address_string.rstrip(', ')

    URL = 'https://geocode.search.hereapi.com/v1/geocode'
    PARAMS = {'apiKey': os.environ['HERE_API_KEY'], 'q': address_string}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return {
        'lng': data['items'][0]['position']['lng'],
        'lat': data['items'][0]['position']['lat'],
    }


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
    ('geolocation', GeolocationForm),
    ('roles', IndividualRolesForm),
    ('more_about_you', IndividualMoreAboutYouForm),
    ('detailed_info', IndividualDetailedInfoForm),
    ('social_networks', IndividualSocialNetworkFormSet),
]

INDIVIDUAL_TEMPLATES = {
    'basic_info': 'maps/profiles/individual/basic_info.html',
    'contact_info': 'maps/profiles/individual/contact_info.html',
    'geolocation': 'maps/profiles/individual/geolocation.html',
    'roles': 'maps/profiles/individual/roles.html',
    'more_about_you': 'maps/profiles/individual/more_about_you.html',
    'detailed_info': 'maps/profiles/individual/detailed_info.html',
    'social_networks': 'maps/profiles/individual/social_networks.html',
}

ORGANIZATION_FORMS = [
    ('org_type', OrganizationTypeForm),
    ('basic_info', OrganizationBasicInfoForm),
    ('contact_info', OrganizationContactInfoForm),
    ('geolocation', GeolocationForm),
    ('detailed_info', OrganizationDetailedInfoForm),
    ('scope_and_impact', OrganizationScopeAndImpactForm),
    ('social_networks', OrganizationSocialNetworkFormSet),
]

ORGANIZATION_TEMPLATES = {
    'org_type': 'maps/profiles/organization/org_type.html',
    'basic_info': 'maps/profiles/organization/basic_info.html',
    'contact_info': 'maps/profiles/organization/contact_info.html',
    'geolocation': 'maps/profiles/organization/geolocation.html',
    'detailed_info': 'maps/profiles/organization/detailed_info.html',
    'scope_and_impact': 'maps/profiles/organization/scope_and_impact.html',
    'social_networks': 'maps/profiles/organization/social_networks.html'
}

TOOL_FORMS = [
    ('basic_info', ToolBasicInfoForm),
    ('detailed_info', ToolDetailedInfoForm)
]

TOOL_TEMPLATES = {
    'basic_info': 'maps/profiles/tool/basic_info.html',
    'detailed_info': 'maps/profiles/tool/detailed_info.html'
}


def show_more_about_you_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('roles') or {'roles': []}
    if (len(cleaned_data['roles']) == 1 and cleaned_data['roles'][0].name == 'Other'):
        return False

    return True


def show_scope_and_impact_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('org_type') or {'type': False}
    if (cleaned_data['type'] and cleaned_data['type'].name == 'Cooperative'):
        return True

    return False


class IndividualProfileWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current in ['more_about_you', 'detailed_info']:
            roles = self.get_cleaned_data_for_step('roles')['roles']
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
                if r.name == 'Community Builder':
                    context.update({'display_community_skills': True})
                if r.name in ['Funder', 'Policymaker']:
                    context.update({'display_affiliation': True})
        return context

    # Attempt to solve SocialNetwork problem on profile pages.
    def get_form_initial(self, step):
        initial = []
        if step == 'social_networks':
            socialnetworks = SocialNetwork.objects.all()
            for index, sn in enumerate(socialnetworks):
                initial.append({
                    'socialnetwork': sn,
                    'name': sn.name,
                    'hint': sn.hint,
                })
            return self.initial_dict.get('social_networks', initial)
        if step == 'geolocation':
            contact_info = self.get_cleaned_data_for_step('contact_info')
            lat_lng = contact_info_to_lng_lat(contact_info)
            return self.initial_dict.get(step, lat_lng)

    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user
        form_dict = self.get_all_cleaned_data()
        form_dict['geom'] = Point(float(form_dict['lng']), float(form_dict['lat']))
        for k, v in form_dict.items():
            if k not in ['roles', 'languages', 'services', 'challenges', 'formset-social_networks', ]:
                setattr(user, k, v)
        user.has_profile = True
        user.save()
        user.roles.set(form_dict['roles'])
        user.languages.set(form_dict['languages'])
        user.services.set(form_dict['services'])
        for org in form_dict['member_of']:
            member_of_relationship = Relationship.objects.get(name="Member of")
            rel = EntitiesEntities(from_ind=user, to_org=org, relationship=member_of_relationship)
            rel.save()
            user.related_organizations.add(org)
        for org in form_dict['founder_of']:
            founder_of_relationship = Relationship.objects.get(name="Founder of")
            rel = EntitiesEntities(from_ind=user, to_org=org, relationship=founder_of_relationship)
            rel.save()
            user.related_organizations.add(org)
        for org in form_dict['worked_with']:
            worked_with_relationship = Relationship.objects.get(name="Worked with")
            rel = EntitiesEntities(from_ind=user, to_org=org, relationship=worked_with_relationship)
            rel.save()
            user.related_organizations.add(org)
        for sn in form_dict['formset-social_networks']:
            if sn['identifier'] != '':
                UserSocialNetwork.objects.create(user=user, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])

        return redirect('individual-detail', user_id=user.id)


class InvididualBasicInfoUpdate(UpdateView):
    model = get_user_model()
    template_name = 'maps/profiles/individual/update_basic_info.html'

    def get_form_class(self):
        return IndividualBasicInfoUpdateForm

    def get_object(self, *args, **kwargs):
        user = super(InvididualBasicInfoUpdate, self).get_object(*args, **kwargs)
        if user != self.request.user:
            raise PermissionDenied()  # TODO: Make this nicer
        return user

    def get_initial(self):
        if self.object.geom:
            return {'lng': self.object.geom.x, 'lat': self.object.geom.y}
        else:
            return {'lat': 0, 'lng': 0}

    def get_success_url(self, **kwargs):
        return reverse('individual-detail', kwargs={'user_id': self.object.id})

    def form_valid(self, form):
        if form.cleaned_data['lat'] and form.cleaned_data['lng']:
            self.object.geom = Point(float(form.cleaned_data['lng']), float(form.cleaned_data['lat']))
        else:
            self.object.geom = Point([])
        return super(InvididualBasicInfoUpdate, self).form_valid(form)


class InvididualOverviewUpdate(UpdateView):
    model = get_user_model()
    template_name = 'maps/profiles/individual/update_overview.html'

    def get_form_class(self):
        return IndividualOverviewUpdateForm

    def get_object(self, *args, **kwargs):
        user = super(InvididualOverviewUpdate, self).get_object(*args, **kwargs)
        if user != self.request.user:
            raise PermissionDenied()  # TODO: Make this nicer
        return user

    def get_context_data(self, **kwargs):
        context = super(InvididualOverviewUpdate, self).get_context_data(**kwargs)
        roles = self.object.roles.all()
        context.update({'roles': roles})
        return context

    def get_initial(self):
        member_of_relationship = Relationship.objects.get(name="Member of")
        member_of_relationships = EntitiesEntities.objects.filter(from_ind=self.object, relationship=member_of_relationship)
        founder_of_relationship = Relationship.objects.get(name="Founder of")
        founder_of_relationships = EntitiesEntities.objects.filter(from_ind=self.object, relationship=founder_of_relationship)
        worked_with_relationship = Relationship.objects.get(name="Worked with")
        worked_with_relationships = EntitiesEntities.objects.filter(from_ind=self.object, relationship=worked_with_relationship)
        member_orgs = []
        founder_orgs = []
        worked_with_orgs = []
        for relationship in member_of_relationships:
            member_orgs.append(Organization.objects.get(id=relationship.to_org.id))
        for relationship in founder_of_relationships:
            founder_orgs.append(Organization.objects.get(id=relationship.to_org.id))
        for relationship in worked_with_relationships:
            worked_with_orgs.append(Organization.objects.get(id=relationship.to_org.id))
        return {
            'member_of': member_orgs,
            'founder_of': founder_orgs,
            'worked_with': worked_with_orgs
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        initial = []
        socialnetworks = SocialNetwork.objects.all()
        for index, sn in enumerate(socialnetworks):
            if sn not in self.object.socialnetworks.all():
                initial.append({
                    'socialnetwork': sn.id,
                    'name': sn.name,
                    'hint': sn.hint,
                })
        social_network_form = IndividualEditSocialNetworkFormSet(instance=self.object, initial=initial)
        return self.render_to_response(self.get_context_data(form=form, social_network_form=social_network_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_network_form = IndividualEditSocialNetworkFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and social_network_form.is_valid()):
            return self.form_valid(form, social_network_form)
        return self.form_invalid(form, social_network_form)

    def get_success_url(self, **kwargs):
        return reverse('individual-detail', kwargs={'user_id': self.object.id})

    def form_valid(self, form, social_network_form):
        member_of_relationship = Relationship.objects.get(name="Member of")
        founder_of_relationship = Relationship.objects.get(name="Founder of")
        worked_with_relationship = Relationship.objects.get(name="Worked with")
        self.object.related_organizations.clear()
        for member_of_org in form.cleaned_data['member_of']:
            EntitiesEntities.objects.create(from_ind=self.object, to_org=member_of_org, relationship=member_of_relationship)
        for founded_by_org in form.cleaned_data['founder_of']:
            EntitiesEntities.objects.create(from_ind=self.object, to_org=founded_by_org, relationship=founder_of_relationship)
        for worked_with_org in form.cleaned_data['worked_with']:
            EntitiesEntities.objects.create(from_ind=self.object, to_org=worked_with_org, relationship=worked_with_relationship)
        self.object.socialnetworks.clear()
        for sn in social_network_form.cleaned_data:
            if sn['identifier'] != '':
                UserSocialNetwork.objects.create(user=self.object, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])
        return super(InvididualOverviewUpdate, self).form_valid(form)


class OrganizationProfileWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [ORGANIZATION_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current in ['basic_info', 'contact_info', 'detailed_info']:
            type = self.get_cleaned_data_for_step('org_type')['type']
            if type.name == 'Cooperative':
                context.update({'is_coop': True})
            elif type.name == 'Potential cooperative':
                context.update({'is_potential_coop': True})
            elif type.name == 'Shared platform':
                context.update({'is_shared_platform': True})
        return context

    # Attempt to solve SocialNetwork problem on profile pages.
    def get_form_initial(self, step):
        initial = []
        if step == 'social_networks':
            socialnetworks = SocialNetwork.objects.all()
            for index, sn in enumerate(socialnetworks):
                initial.append({
                    'socialnetwork': sn,
                    'name': sn.name,
                    'hint': sn.hint,
                })
            return self.initial_dict.get('social_networks', initial)
        if step in ['basic_info', 'contact_info', 'detailed_info']:
            org_type_data = self.get_cleaned_data_for_step('org_type')
            return self.initial_dict.get(step, {'type': org_type_data['type']})
        if step == 'geolocation':
            contact_info = self.get_cleaned_data_for_step('contact_info')
            lat_lng = contact_info_to_lng_lat(contact_info)
            return self.initial_dict.get(step, lat_lng)

    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user
        form_dict = self.get_all_cleaned_data()
        form_dict['geom'] = Point(float(form_dict['lng']), float(form_dict['lat']))
        org = Organization(admin_email=user.email)
        for k, v in form_dict.items():
            if k not in ['languages', 'categories', 'sectors', 'formset-social_networks']:
                setattr(org, k, v)
        setattr(org, 'type_id', form_dict['type'].id)
        org.save()
        org.languages.set(form_dict['languages'])
        if form_dict['type'].name == 'Cooperative':
            # We don't need to set these for non-coops at present.
            org.categories.set(form_dict['categories'])
        org.sectors.set(form_dict['sectors'])
        for sn in form_dict['formset-social_networks']:
            if sn['identifier'] != '':
                OrganizationSocialNetwork.objects.create(organization=org, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])

        return redirect('organization-detail', organization_id=org.id)


class OrganizationBasicInfoUpdate(UpdateView):
    model = Organization
    template_name = 'maps/profiles/organization/update_basic_info.html'

    def get_form_class(self):
        return OrganizationBasicInfoUpdateForm

    def get_object(self, *args, **kwargs):
        org = super(OrganizationBasicInfoUpdate, self).get_object(*args, **kwargs)
        if org.admin_email != self.request.user.email:
            raise PermissionDenied()  # TODO: Make this nicer
        return org

    def get_initial(self):
        return {}

    def get_success_url(self, **kwargs):
        return reverse('organization-detail', kwargs={'organization_id': self.object.id})

    def form_valid(self, form):
        return super(OrganizationBasicInfoUpdate, self).form_valid(form)


class OrganizationOverviewUpdate(UpdateView):
    model = Organization
    template_name = 'maps/profiles/organization/update_overview.html'

    def get_form_class(self):
        return OrganizationOverviewUpdateForm

    def get_object(self, *args, **kwargs):
        org = super(OrganizationOverviewUpdate, self).get_object(*args, **kwargs)
        if org.admin_email != self.request.user.email:
            raise PermissionDenied()  # TODO: Make this nicer
        return org

    def get_initial(self):
        year = ''
        month = ''
        day = ''

        if self.object.founded:
            pieces = str(self.object.founded).split('-')
            year = pieces[0]
            month = pieces[1]
            day = pieces[2]
        elif self.object.founded_min_date and self.object.founded_max_date:
            min_pieces = str(self.object.founded_min_date).split('-')
            max_pieces = str(self.object.founded_max_date).split('-')
            year = min_pieces[0]
            if min_pieces[1] == max_pieces[1]:
                month = min_pieces[1]

        return {
            'year_founded': year,
            'month_founded': month,
            'day_founded': day,
            'type': self.object.type
        }

    def get_success_url(self, **kwargs):
        return reverse('organization-detail', kwargs={'organization_id': self.object.id})

    def form_valid(self, form):
        return super(OrganizationOverviewUpdate, self).form_valid(form)


class OrganizationContactUpdate(UpdateView):
    model = Organization
    template_name = 'maps/profiles/organization/update_contact.html'

    def get_form_class(self):
        return OrganizationContactUpdateForm

    def get_object(self, *args, **kwargs):
        org = super(OrganizationContactUpdate, self).get_object(*args, **kwargs)
        if org.admin_email != self.request.user.email:
            raise PermissionDenied()  # TODO: Make this nicer
        return org

    def get_initial(self):
        lng = 0
        lat = 0

        if self.object.geom:
            lng = self.object.geom.x
            lat = self.object.geom.y

        return {
            'lat': lat,
            'lng': lng
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        initial = []
        socialnetworks = SocialNetwork.objects.all()
        for index, sn in enumerate(socialnetworks):
            if sn not in self.object.socialnetworks.all():
                initial.append({
                    'socialnetwork': sn.id,
                    'name': sn.name,
                    'hint': sn.hint,
                })
        social_network_form = OrganizationEditSocialNetworkFormSet(instance=self.object, initial=initial)
        return self.render_to_response(self.get_context_data(form=form, social_network_form=social_network_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_network_form = OrganizationEditSocialNetworkFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and social_network_form.is_valid()):
            return self.form_valid(form, social_network_form)
        return self.form_invalid(form, social_network_form)

    def get_success_url(self, **kwargs):
        return reverse('organization-detail', kwargs={'organization_id': self.object.id})

    def form_valid(self, form, social_network_form):
        if form.cleaned_data['lat'] and form.cleaned_data['lng']:
            self.object.geom = Point(float(form.cleaned_data['lng']), float(form.cleaned_data['lat']))
        else:
            self.object.geom = Point([])
        self.object.socialnetworks.clear()
        for sn in social_network_form.cleaned_data:
            if sn['identifier'] != '':
                OrganizationSocialNetwork.objects.create(organization=self.object, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])
        return super(OrganizationContactUpdate, self).form_valid(form)


class ToolWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [TOOL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'basic_info':
            niche_dict = {}
            niches = Niche.objects.all()
            for niche in niches:
                parent = niche.parent()
                if parent not in niche_dict:
                    niche_dict[parent] = {'children': []}
                if niche.child():
                    niche_dict[parent]['children'].append({'id': niche.id, 'name': niche.child()})
                else:
                    niche_dict[parent]['id'] = niche.id
            context.update({'niche_dict': niche_dict})
        return context

    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user
        form_dict = self.get_all_cleaned_data()
        tool = Tool(submitted_by_email=user.email)
        for k, v in form_dict.items():
            if k not in ['niches', 'sectors', 'languages_supported']:
                setattr(tool, k, v)
        tool.save()
        tool.niches.set(form_dict['niches'])
        tool.sectors.set(form_dict['sectors'])
        tool.languages_supported.set(form_dict['languages_supported'])
        messages.success(self.request, 'Thank you for submitting this tool.')
        return HttpResponseRedirect('/my-profiles/')


def index(request):
    template = loader.get_template('maps/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# Organization
def organization_detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    member_of_relationship = Relationship.objects.get(name="Member of")
    member_of_relationships = EntitiesEntities.objects.filter(to_org=organization, relationship=member_of_relationship)
    founder_of_relationship = Relationship.objects.get(name="Founder of")
    founder_of_relationships = EntitiesEntities.objects.filter(to_org=organization, relationship=founder_of_relationship)
    members = []
    founders = []
    for relationship in member_of_relationships:
        members.append(get_user_model().objects.get(id=relationship.from_ind.id))
    for relationship in founder_of_relationships:
        founders.append(get_user_model().objects.get(id=relationship.from_ind.id))

    context = {
        'organization': organization,
        'members': members,
        'founders': founders
    }
    return render(request, 'maps/organization_detail.html', context)


# Individual
def individual_detail(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    member_of_relationship = Relationship.objects.get(name="Member of")
    member_of_relationships = EntitiesEntities.objects.filter(from_ind=user, relationship=member_of_relationship)
    founder_of_relationship = Relationship.objects.get(name="Founder of")
    founder_of_relationships = EntitiesEntities.objects.filter(from_ind=user, relationship=founder_of_relationship)
    worked_with_relationship = Relationship.objects.get(name="Worked with")
    worked_with_relationships = EntitiesEntities.objects.filter(from_ind=user, relationship=worked_with_relationship)
    member_orgs = []
    founder_orgs = []
    worked_with_orgs = []
    for relationship in member_of_relationships:
        member_orgs.append(Organization.objects.get(id=relationship.to_org.id))
    for relationship in founder_of_relationships:
        founder_orgs.append(Organization.objects.get(id=relationship.to_org.id))
    for relationship in worked_with_relationships:
        worked_with_orgs.append(Organization.objects.get(id=relationship.to_org.id))
    context = {
        'individual': user,
        'member_orgs': member_orgs,
        'founder_orgs': founder_orgs,
        'worked_with_orgs': worked_with_orgs
    }
    return render(request, 'maps/individual_detail.html', context)


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('my-profiles')
    success_message = "You have successfully deleted the organizational profile for %(name)s."

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(OrganizationDelete, self).delete(request, *args, **kwargs)

# My Profiles


@ login_required
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


@ login_required
def account_settings(request):
    return render(request, 'maps/account_settings.html')

# Static pages


class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"


class AboutPageView(TemplateView):
    template_name = "maps/about.html"
