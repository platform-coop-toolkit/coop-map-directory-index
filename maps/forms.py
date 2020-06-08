from django.contrib.auth import get_user_model
from django import forms
from django.forms import CharField, CheckboxSelectMultiple, RadioSelect, SelectMultiple, HiddenInput, formset_factory
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from django.template.defaultfilters import safe
from accounts.models import Role, SocialNetwork, UserSocialNetwork
from mdi.models import Organization, Category, Language

class BaseForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'

        super(BaseForm, self).__init__(*args, **kwargs)


class BaseModelForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'

        super(BaseModelForm, self).__init__(*args, **kwargs)

# Individual forms.

class IndividualBasicInfoForm(BaseModelForm):
    first_name = CharField(
        required=True,
        label=_('First name')
    )
    last_name = CharField(
        required=True,
        label=_('Last name')
    )
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=True,
        label=_('Languages you speak'),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'languages',
        ]
        labels = {
            'middle_name': _('Middle name')
        }

class IndividualContactInfoForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'url',
            'email',
            'phone',
            'address',
            'city', # TODO: required
            'state', # TODO: required
            'country', # TODO: required
            'postal_code'
        ]
        labels = {
            'email': _('Email'),
            'url': _('Website address'),
            'address': _('Street address'),
            'city': _('City or town'),
            'state': _('State or province'),
            'postal_code': _('ZIP or postal code')
        }

class IndividualRolesForm(BaseForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        label=safe('How would you describe yourself?'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
    )


class IndividualMoreAboutYouForm(BaseModelForm):
    member_of = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label=_('Co-operative(s) you are a currently a member of'),
        required=False
    )

    founder_of = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label=_('Co-operative(s) you are a founder of'),
        required=False
    )

    worked_with = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label=_('Co-operative(s) you have worked with'),
        required=False
    )
    class Meta:
        model = get_user_model()
        fields = [
            'member_of',
            'founder_of',
            'worked_with',
            'services',
            # TODO: Add community skills
            'field_of_study',
            'affiliation',
            # TODO: Add URL for affiliated organization
        ]
        labels = {
            'worked_with': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'services': _('Services you provide'),
            'field_of_study': _('What is your field of research?'),
            'affiliation': _('Are you affiliated with a research organisation or institution?'),
        }
        widgets = {
            'member_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'founder_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'services': SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        }
class IndividualDetailedInfoForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'bio',
            'projects',
        ]
        labels = {
            'bio': _('Bio'),
            'projects': _('Projects'),
        }
        help_texts = {
            'bio': _('Share a bit about yourself.'),
            'projects': _('List any current or past projects you would like to share with others.')
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

class OrganizationBasicInfoForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'languages'
        ]
        labels = {
            'name': _('Name of cooperative'),
            'languages': _('Working languages')
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
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'url': _('Website address'),
            'email': _('Email'),
            'city': _('City or town'),
            'country': _('Country'),
            'state': _('State or province'),
            'address': _('Street address'),
            'postal_code': _('ZIP or postal code')
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
            'categories': _('Co-op type'),
            'num_workers': _('Number of workers'),
            'num_members': _('Number of members'),
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
