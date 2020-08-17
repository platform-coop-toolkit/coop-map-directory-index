from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum, Count, Q, Value
from django.db.models.functions import Concat
from django_countries import countries
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory  # ModelMultipleChoiceField, SelectMultiple
from accounts.models import UserSocialNetwork
from mdi.models import Organization, SocialNetwork, OrganizationSocialNetwork, Relationship, EntitiesEntities, \
    Tool, Niche, Type, Sector, Source
from formtools.wizard.views import SessionWizardView
from .forms import GeolocationForm, IndividualProfileDeleteForm, IndividualRolesForm, IndividualBasicInfoForm, \
    IndividualMoreAboutYouForm, IndividualDetailedInfoForm, IndividualContactInfoForm, IndividualSocialNetworkFormSet, \
    IndividualEditSocialNetworkFormSet, IndividualOverviewUpdateForm, IndividualBasicInfoUpdateForm, \
    OrganizationTypeForm, OrganizationBasicInfoForm, OrganizationContactInfoForm, OrganizationDetailedInfoForm, \
    OrganizationScopeAndImpactForm, OrganizationSocialNetworkFormSet, OrganizationBasicInfoUpdateForm, \
    OrganizationOverviewUpdateForm, OrganizationContactUpdateForm, OrganizationEditSocialNetworkFormSet, \
    ToolBasicInfoForm, ToolDetailedInfoForm, ToolUpdateForm
from django_countries import countries
from django.contrib.gis.geos import Point
import os
import requests


class RedirectMixin:
    redirect_url = None
    redirect_message = None

    def get_redirect_message(self):
        redirect_message = self.redirect_message
        if not redirect_message:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_message attribute. Define {0}.redirect_message or override '
                '{0}.get_redirect_message().'.format(self.__class__.__name__)
            )
        return str(redirect_message)

    def get_redirect_url(self):
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
                '{0}.get_redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        test_result = self.get_test_func()()
        if not test_result:
            messages.error(self.request, self.get_redirect_message())
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class IndividualProfileRedirectMixin(RedirectMixin):
    def test_func(self):
        if self.request.user.has_profile:
            return False
        return True


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


class IndividualProfileWizard(LoginRequiredMixin, IndividualProfileRedirectMixin, SessionWizardView):
    redirect_url = reverse_lazy('my-profiles')
    redirect_message = _('You already have an individual profile.')

    def get_template_names(self):
        return [INDIVIDUAL_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({
            'labels': {
                'cancelTitle': _('Cancel'),
                'cancelQuestion': _('Are you sure you want to exit the profile editor and discard all of your information?'),
                'cancelConfirm': _('Yes, exit and discard all info'),
                'cancelDismiss': _('No, return to profile editor')
            }
        })
        context.update({'profile_type': 'individual'})

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
        organic = Source.objects.get(name='Organic')
        user.source = organic
        user.save()
        user.roles.set(form_dict['roles'])
        user.languages.set(form_dict['languages'])
        if 'services' in form_dict:
            user.services.set(form_dict['services'])
        if 'member_of' in form_dict:
            for org in form_dict['member_of']:
                member_of_relationship = Relationship.objects.get(name="Member of")
                rel = EntitiesEntities(from_ind=user, to_org=org, relationship=member_of_relationship)
                rel.save()
                user.related_organizations.add(org)
        if 'founder_of' in form_dict:
            for org in form_dict['founder_of']:
                founder_of_relationship = Relationship.objects.get(name="Founder of")
                rel = EntitiesEntities(from_ind=user, to_org=org, relationship=founder_of_relationship)
                rel.save()
                user.related_organizations.add(org)
        if 'worked_with' in form_dict:
            for org in form_dict['worked_with']:
                worked_with_relationship = Relationship.objects.get(name="Worked with")
                rel = EntitiesEntities(from_ind=user, to_org=org, relationship=worked_with_relationship)
                rel.save()
                user.related_organizations.add(org)
        for sn in form_dict['formset-social_networks']:
            if sn['identifier'] != '':
                UserSocialNetwork.objects.create(user=user, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])

        return redirect('individual-detail', user_id=user.id)


class InvididualBasicInfoUpdate(LoginRequiredMixin, UpdateView):
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


class InvididualOverviewUpdate(LoginRequiredMixin, UpdateView):
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
        context.update({
            'labels': {
                'cancelTitle': _('Cancel'),
                'cancelQuestion': _('Are you sure you want to exit the profile editor and discard all of your information?'),
                'cancelConfirm': _('Yes, exit and discard all info'),
                'cancelDismiss': _('No, return to profile editor')
            }
        })
        context.update({'profile_type': 'organization'})

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
        organic = Source.objects.get(name='Organic')
        org.source = organic
        org.save()
        org.languages.set(form_dict['languages'])
        if form_dict['type'].name == 'Cooperative':
            # We don't need to set these for non-coops at present.
            org.categories.set(form_dict['categories'])
        if 'sectors' in form_dict:
            org.sectors.set(form_dict['sectors'])
        for sn in form_dict['formset-social_networks']:
            if sn['identifier'] != '':
                OrganizationSocialNetwork.objects.create(organization=org, socialnetwork=sn['socialnetwork'], identifier=sn['identifier'])

        return redirect('organization-detail', organization_id=org.id)


class OrganizationBasicInfoUpdate(LoginRequiredMixin, UpdateView):
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


class OrganizationOverviewUpdate(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'maps/profiles/organization/update_overview.html'

    def get_form_class(self):
        return OrganizationOverviewUpdateForm

    def get_object(self, *args, **kwargs):
        org = super(OrganizationOverviewUpdate, self).get_object(*args, **kwargs)
        if org.admin_email != self.request.user.email:
            raise PermissionDenied()  # TODO: Make this nicer
        return org

    def get_context_data(self, **kwargs):
        context = super(OrganizationOverviewUpdate, self).get_context_data(**kwargs)
        type = self.object.type
        context.update({'type': type})
        return context

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


class OrganizationContactUpdate(LoginRequiredMixin, UpdateView):
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

    def get_form_initial(self, step):
        if step == 'basic_info':
            if self.request.method == 'POST':
                return self.initial_dict.get(step, {'niches': [int(x) for x in self.request.POST.getlist('basic_info-niches')]})
            return self.initial_dict.get(step)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({'profile_type': 'tool'})
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


class ToolUpdate(LoginRequiredMixin, UpdateView):
    model = Tool
    template_name = 'maps/profiles/tool/update.html'

    def get_form_class(self):
        return ToolUpdateForm

    def get_initial(self):
        if self.object.niches:
            niches = []
            for niche in self.object.niches.all():
                niches.append(niche.id)
            return {
                'niches': niches
            }
        return {}

    def get_context_data(self, **kwargs):
        context = super(ToolUpdate, self).get_context_data(**kwargs)
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


class SearchResultsView(ListView):
    model = Organization
    template_name = 'maps/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('s')
        object_list = Organization.objects.filter(
            Q(name__icontains=query) | Q(type__name__icontains=query) | Q(sectors__name__icontains=query) | Q(categories__name__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query) | Q(state__icontains=query) | Q(country__exact=query) | Q(legal_status__name__icontains=query)
        ).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('s')
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        individual_list = get_user_model().objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(has_profile=True).filter(
            Q(full_name__icontains=query) | Q(roles__name__icontains=query) | Q(bio__icontains=query) | Q(city__icontains=query) | Q(state__icontains=query) | Q(country__exact=query) | Q(affiliation__icontains=query)
        )
        context.update({
            'search_term': query,
            'individual_list': individual_list
        })
        return context

# My Profiles


@login_required
def my_profiles(request):
    user = request.user
    user_orgs = Organization.objects.filter(admin_email=user.email)

    if request.method == 'POST':
        form = IndividualProfileDeleteForm(request.POST, instance=user)
        if form.is_valid():
            fields = [
                'address',
                'affiliation_url',
                'affiliation',
                'bio',
                'city',
                'community_skills',
                'country',
                'field_of_study',
                'first_name',
                'geom',
                'last_name',
                'middle_name',
                'notes'
                'phone',
                'postal_code',
                'projects',
                'state',
                'url',
            ]

            for f in filter(lambda x: x.name in fields, user._meta.fields):
                if f.blank or f.has_default():
                    setattr(user, f.name, f.get_default())

            user.challenges.clear()
            user.languages.clear()
            user.related_organizations.clear()
            user.roles.clear()
            user.services.clear()
            user.socialnetworks.clear()
            user.save()
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


class SummaryPageView(TemplateView):
    template_name = "maps/summary_of_impact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chart_labels = [
            _('Unknown'),
            _('Local'),
            _('Regional'),
            _('National'),
            _('International')
        ]

        chart_colors = [
            '#edf5f3',
            '#c9f8db',
            '#face00',
            '#ff621a',
            '#1d7c79'
        ]

        chart_defaults = [
            0,
            0,
            0,
            0,
            0
        ]

        context['labels'] = {
            'countries': _('Apply filter by country'),
            'org_type': _('Apply filter by organization type'),
            'coops': _('Co-ops'),
            'coops_in': _('Co-ops in %s'),
            'coops_plus': _('Co-ops, potential co-ops and shared platforms'),
            'coops_plus_in': _('Co-ops, potential co-ops and shared platforms in %s'),
            'supporting_orgs': _('Supporting organizations'),
            'supporting_orgs_in': _('Supporting organizations in %s'),
            'workers': _('workers'),
            'members': _('members'),
            'sectors': _('sectors'),
            'impacted': _('people impacted'),
            'geo_scope': _('Geographic scope of %s'),
            'geo_scope_in': _('Geographic scope of %s in %s')
        }

        context['colors'] = chart_colors

        coop_type = Type.objects.get(name='Cooperative')
        potential_coop_type = Type.objects.get(name='Potential cooperative')
        shared_platform_type = Type.objects.get(name='Shared platform')
        supporting_org_type = Type.objects.get(name='Supporting organization')

        context['countries'] = {'ALL': {'name': _('All')}}

        coops = Organization.objects.filter(type=coop_type)
        coop_impact = coops.aggregate(people_impacted=Sum('impacted_exact_number', distinct=True), workers=Sum('num_workers', distinct=True), members=Sum('num_members', distinct=True), sectors=Count('sectors', distinct=True))
        coop_impact['count'] = coops.count()
        coop_scopes = {
            'unknown': coops.filter(geo_scope__exact='').count(),
            'local': coops.filter(geo_scope__exact='Local').count(),
            'regional': coops.filter(geo_scope__exact='Regional').count(),
            'national': coops.filter(geo_scope__exact='National').count(),
            'international': coops.filter(geo_scope__exact='International').count()
        }
        coop_impact['scope'] = {
            'datasets': [
                {
                    'data': [
                        coop_scopes['unknown'],
                        coop_scopes['local'],
                        coop_scopes['regional'],
                        coop_scopes['national'],
                        coop_scopes['international']
                    ],
                    'backgroundColor': chart_colors
                }
            ],
            'labels': chart_labels
        }

        coops_plus = Organization.objects.filter(type__in=[coop_type, potential_coop_type, shared_platform_type])
        coops_plus_impact = coops_plus.aggregate(people_impacted=Sum('impacted_exact_number', distinct=True), workers=Sum('num_workers', distinct=True), members=Sum('num_members', distinct=True), sectors=Count('sectors', distinct=True))
        coops_plus_impact['count'] = coops_plus.count()
        coops_plus_impact['sectors'] = Sector.objects.filter(organization__in=coops_plus).distinct().count()
        coops_plus_scopes = {
            'unknown': coops_plus.filter(geo_scope__exact='').count(),
            'local': coops_plus.filter(geo_scope__exact='Local').count(),
            'regional': coops_plus.filter(geo_scope__exact='Regional').count(),
            'national': coops_plus.filter(geo_scope__exact='National').count(),
            'international': coops_plus.filter(geo_scope__exact='International').count()
        }
        coops_plus_impact['scope'] = {
            'datasets': [
                {
                    'data': [
                        coops_plus_scopes['unknown'],
                        coops_plus_scopes['local'],
                        coops_plus_scopes['regional'],
                        coops_plus_scopes['national'],
                        coops_plus_scopes['international']
                    ],
                    'backgroundColor': chart_colors
                }
            ],
            'labels': chart_labels
        }

        supporting_orgs = Organization.objects.filter(type=supporting_org_type)
        supporting_orgs_impact = supporting_orgs.aggregate(workers=Sum('num_workers', distinct=True), sectors=Count('sectors', distinct=True))
        supporting_orgs_impact['count'] = supporting_orgs.count()
        supporting_orgs_scopes = {
            'unknown': supporting_orgs.filter(geo_scope__exact='').count(),
            'local': supporting_orgs.filter(geo_scope__exact='Local').count(),
            'regional': supporting_orgs.filter(geo_scope__exact='Regional').count(),
            'national': supporting_orgs.filter(geo_scope__exact='National').count(),
            'international': supporting_orgs.filter(geo_scope__exact='International').count()
        }
        supporting_orgs_impact['scope'] = {
            'datasets': [
                {
                    'data': [
                        supporting_orgs_scopes['unknown'],
                        supporting_orgs_scopes['local'],
                        supporting_orgs_scopes['regional'],
                        supporting_orgs_scopes['national'],
                        supporting_orgs_scopes['international']
                    ],
                    'backgroundColor': chart_colors
                }
            ],
            'labels': chart_labels
        }

        context['countries']['ALL']['coops'] = coop_impact
        context['countries']['ALL']['coops_plus'] = coops_plus_impact
        context['countries']['ALL']['supporting_orgs'] = supporting_orgs_impact

        for key, country in dict(countries).items():
            context['countries'][key] = {'name': country}
            coops = Organization.objects.filter(country__exact=key, type=coop_type)
            if coops.count() > 0:
                coop_impact = coops.aggregate(people_impacted=Sum('impacted_exact_number', distinct=True), workers=Sum('num_workers', distinct=True), members=Sum('num_members', distinct=True), sectors=Count('sectors', distinct=True))
                coop_impact['count'] = coops.count()
                coop_scopes = {
                    'unknown': coops.filter(geo_scope__exact='').count(),
                    'local': coops.filter(geo_scope__exact='Local').count(),
                    'regional': coops.filter(geo_scope__exact='Regional').count(),
                    'national': coops.filter(geo_scope__exact='National').count(),
                    'international': coops.filter(geo_scope__exact='International').count()
                }
                coop_impact['scope'] = {
                    'datasets': [
                        {
                            'data': [
                                coop_scopes['unknown'],
                                coop_scopes['local'],
                                coop_scopes['regional'],
                                coop_scopes['national'],
                                coop_scopes['international']
                            ],
                            'backgroundColor': chart_colors
                        }
                    ],
                    'labels': chart_labels
                }
                context['countries'][key]['coops'] = coop_impact
            else:
                coop_impact = None
                context['countries'][key]['coops'] = {
                    'people_impacted': 0,
                    'workers': 0,
                    'members': 0,
                    'sectors': 0,
                    'count': 0,
                    'scope': {
                        'datasets': [
                            {
                                'data': chart_defaults,
                                'backgroundColor': chart_colors
                            }
                        ],
                        'labels': chart_labels
                    }
                }

            coops_plus = Organization.objects.filter(country__exact=key, type__in=[coop_type, potential_coop_type, shared_platform_type])
            if coops_plus.count() > 0:
                coops_plus_impact = coops_plus.aggregate(people_impacted=Sum('impacted_exact_number', distinct=True), workers=Sum('num_workers', distinct=True), members=Sum('num_members', distinct=True), sectors=Count('sectors', distinct=True))
                coops_plus_impact['count'] = coops_plus.count()
                coops_plus_scopes = {
                    'unknown': coops_plus.filter(geo_scope__exact='').count(),
                    'local': coops_plus.filter(geo_scope__exact='Local').count(),
                    'regional': coops_plus.filter(geo_scope__exact='Regional').count(),
                    'national': coops_plus.filter(geo_scope__exact='National').count(),
                    'international': coops_plus.filter(geo_scope__exact='International').count()
                }
                coops_plus_impact['scope'] = {
                    'datasets': [
                        {
                            'data': [
                                coops_plus_scopes['unknown'],
                                coops_plus_scopes['local'],
                                coops_plus_scopes['regional'],
                                coops_plus_scopes['national'],
                                coops_plus_scopes['international']
                            ],
                            'backgroundColor': chart_colors
                        }
                    ],
                    'labels': chart_labels
                }
                context['countries'][key]['coops_plus'] = coops_plus_impact
            else:
                coops_plus_impact = None
                context['countries'][key]['coops_plus'] = {
                    'people_impacted': 0,
                    'workers': 0,
                    'members': 0,
                    'sectors': 0,
                    'count': 0,
                    'scope': {
                        'datasets': [
                            {
                                'data': chart_defaults,
                                'backgroundColor': chart_colors
                            }
                        ],
                        'labels': chart_labels
                    }
                }

            supporting_orgs = Organization.objects.filter(country__exact=key, type=supporting_org_type)
            if supporting_orgs.count() > 0:
                supporting_orgs_impact = supporting_orgs.aggregate(workers=Sum('num_workers', distinct=True), sectors=Count('sectors', distinct=True))
                supporting_orgs_impact['count'] = supporting_orgs.count()
                supporting_orgs_scopes = {
                    'unknown': supporting_orgs.filter(geo_scope__exact='').count(),
                    'local': supporting_orgs.filter(geo_scope__exact='Local').count(),
                    'regional': supporting_orgs.filter(geo_scope__exact='Regional').count(),
                    'national': supporting_orgs.filter(geo_scope__exact='National').count(),
                    'international': supporting_orgs.filter(geo_scope__exact='International').count()
                }
                supporting_orgs_impact['scope'] = {
                    'datasets': [
                        {
                            'data': [
                                supporting_orgs_scopes['unknown'],
                                supporting_orgs_scopes['local'],
                                supporting_orgs_scopes['regional'],
                                supporting_orgs_scopes['national'],
                                supporting_orgs_scopes['international']
                            ],
                            'backgroundColor': chart_colors
                        }
                    ],
                    'labels': chart_labels
                }
                context['countries'][key]['supporting_orgs'] = supporting_orgs_impact
            else:
                supporting_orgs_impact = None
                context['countries'][key]['supporting_orgs'] = {
                    'workers': 0,
                    'sectors': 0,
                    'count': 0,
                    'scope': {
                        'datasets': [
                            {
                                'data': chart_defaults,
                                'backgroundColor': chart_colors
                            }
                        ],
                        'labels': chart_labels
                    }
                }

            if coop_impact == None and coops_plus_impact == None and supporting_orgs_impact == None:
                del context['countries'][key]

        return context
