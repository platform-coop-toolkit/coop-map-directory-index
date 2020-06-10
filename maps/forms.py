from django.contrib.auth import get_user_model
from django import forms
from django.forms import CharField, CheckboxSelectMultiple, IntegerField, ModelChoiceField, RadioSelect, SelectMultiple, HiddenInput, formset_factory
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from django.template.defaultfilters import safe
from django_countries.fields import CountryField
from accounts.models import Role, SocialNetwork, UserSocialNetwork
from mdi.models import Organization, Category, Language, OrganizationSocialNetwork, Stage

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
            'url'
        ]
        labels = {
            'middle_name': _('Middle name'),
            'url': _('Website address')
        }

class IndividualContactInfoForm(BaseModelForm):
    city = CharField(
        required=True,
        label=_('City or town')
    )
    state = CharField(
        required=True,
        label=_('State or province')
    )
    country = CountryField(blank=False).formfield()
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'email': _('Email'),
            'address': _('Street address'),
            'postal_code': _('ZIP or postal code')
        }
        widgets = {

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
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
    )

    founder_of = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label=_('Co-operative(s) you are a founder of'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
    )

    worked_with = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label=_('Co-operative(s) you have worked with'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
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
            'affiliation_url'
        ]
        labels = {
            'worked_with': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'services': _('Services you provide'),
            'field_of_study': _('What is your field of research?'),
            'affiliation': _('Are you affiliated with an organisation or institution?'),
            'affiliation_url': _('What is the website address of your affiliated organisation or institution?'),
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

class OrganizationTypeForm(BaseForm):
    org_type = forms.ChoiceField(
        choices=[
            ('1', 'Cooperative'),
            ('2', 'Business Looking to Convert to a Co-operative')
        ],
        initial='1',
        label=_('How would you describe your organization?'),
        required=True,
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )
class OrganizationBasicInfoForm(BaseModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=True,
        label=_('Working languages'),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )
    class Meta:
        model = Organization
        fields = [
            'name',
            'languages',
            'url'
        ]
        labels = {
            'name': _('Name of cooperative'),
            'url': _('Website address')
        }
        help_texts = {
            'languages': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
        }

class OrganizationContactInfoForm(BaseModelForm):
    city = CharField(
        required=True,
        label=_('City or town')
    )
    state = CharField(
        required=True,
        label=_('State or province')
    )
    country = CountryField(blank=False).formfield()
    class Meta:
        model = Organization
        fields = [
            'email',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'email': _('Email'),
            'address': _('Street address'),
            'postal_code': _('ZIP or postal code')
        }

class OrganizationDetailedInfoForm(BaseModelForm):
    num_workers = IntegerField(
        required=True,
        label=_('Number of workers'),
        help_text=_('Please provide your best estimate.')
    )

    num_members = IntegerField(
        required=True,
        label=_('Number of members'),
        help_text=_('Please provide your best estimate.')
    )

    stage = ModelChoiceField(
        Stage.objects.all(),
        empty_label=_('Not sure'),
        required=False,
        widget=RadioSelect(attrs={'class': 'input-group radio'}),
        label=_('Stage of development')
    )

    worker_distribution = forms.ChoiceField(
        choices=[
            ('', _('Not sure')),
            ('colocated', _('Co-located')),
            ('regional', _('Regionally distributed')),
            ('national', _('Nationally distributed')),
            ('international', _('Internationally distributed'))
        ],
        required=False,
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )
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
        }
        widgets = {
            'categories': CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
            # 'stage': RadioSelect(attrs={'class': 'input-group radio'}),
            # 'worker_distribution': RadioSelect(attrs={'class': 'input-group radio'})
        }
        help_texts = {
            'sectors': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
      }

class OrganizationSocialNetworkForm(BaseModelForm):
    class Meta:
        model = OrganizationSocialNetwork
        fields = [
            'socialnetwork',
            'identifier',
        ]
        widgets = {
            'socialnetwork': HiddenInput(),
        }

OrganizationSocialNetworkFormSet = formset_factory(OrganizationSocialNetworkForm, extra=0)
