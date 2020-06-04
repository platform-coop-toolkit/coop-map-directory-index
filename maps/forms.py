from django.contrib.auth import get_user_model
from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect, SelectMultiple, HiddenInput, formset_factory
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from django.template.defaultfilters import safe
from accounts.models import Role, SocialNetwork, UserSocialNetwork
from mdi.models import Organization, Category


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)

class OrganizationBasicInfoForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'languages'
        ]
        labels = {
            'name': _('Name of cooperative (required)'),
            'languages': _('Working languages (required)')
        }
        widgets = {
            'languages': SelectMultiple(attrs={'required': ''}),
        }
        help_texts = {
            'languages': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
        }

class OrganizationContactInfoForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'url',
            'email',
            'phone',
            'address',
            'city',
            'country',
            'state',
            'postal_code'
        ]
        labels = {
            'url': _('Website address'),
            'email': _('Email (required)'),
            'city': _('City or town'),
            'country': _('Country (required)'),
            'state': _('State or province')
        }

class OrganizationDetailedInfoForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'sectors',
            'categories',
            'num_workers',
            'num_members',
            'stage',
            'worker_distribution'
        ]
        labels = {
            'sectors': _('Co-op sector'),
            'categories': _('Co-op type (required)'),
            'num_workers': _('Number of workers (required)'),
            'num_members': _('Number of members (required)'),
            'stage': _('Stage of development')
        }
        widgets = {
            'categories': CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
            'stage': RadioSelect(attrs={'class': 'input-group radio'}),
            'worker_distribution': RadioSelect(attrs={'class': 'input-group radio'})
        }
        help_texts = {
            'sectors': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
            'num_workers': _('Please provide your best estimate.'),
            'num_members': _('Please provide your best estimate.')
      }


class IndividualRolesForm(BaseForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        label=safe('How would you describe yourself?'),
        help_text=safe('Choose all that apply.'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
    )

class IndividualBasicInfoForm(BaseModelForm):
    member_of = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label='Name of your co-operative',
        required=False
    )
    founder_of = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label='Name of co-ops you have founded',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', # TODO: make this required
            'middle_name',
            'last_name', # TODO: make this required
            'languages',
            'member_of',
            'founder_of',
        ]
        labels = {
            'first_name': _('First name (required)'),
            'middle_name': _('Middle name'),
            'last_name': _('Last name (required)'),
            'languages': _('Language(s) you speak (required)'),
        }
        widgets = {
            'languages': SelectMultiple(attrs={'required': ''}),
            'member_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'founder_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
        }
        help_texts = {
            'languages': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
        }


class IndividualDetailedInfoForm(BaseModelForm):
    worked_with = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label='Coops you have worked/work with',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = [
            'bio',
            'services',
            'worked_with',
            'field_of_study',
            'affiliation',
            'projects',
            'challenges',
        ]
        labels = {
            'bio': _('Share a bit about yourself'),
            'services': _('Services you provide'),
            'field_of_study': _('Your field of study'),
            'affiliation': _('Affiliation'),
            'projects': _('Projects'),
            'challenges': _('Challenges you are facing'),
        }
        widgets = {
            'services': SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
            'worked_with': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'challenges': SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        }


class IndividualContactInfoForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            'url',
        ]
        labels = {
            'address': _('Street address'),
            'url': _('Website address (link)')
        }


class IndividualSocialNetworkForm(BaseModelForm):
    class Meta:
        model = UserSocialNetwork
        fields = [
            'socialnetwork',
            'identifier',
        ]
        widgets = {
            'socialnetwork': HiddenInput(),
        }


IndividualSocialNetworkFormSet = formset_factory(IndividualSocialNetworkForm, extra=0)
