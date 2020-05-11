from django import forms
from django.forms import CheckboxSelectMultiple, DateTimeInput, HiddenInput, RadioSelect, SelectMultiple, \
    URLInput, formset_factory
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import safe
from accounts.models import User, Role
from mdi.models import Organization, OrganizationSocialNetwork, Sector, SocialNetwork, Stage
from datetime import date
from django.utils import timezone


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        years = [(0, 'Select a year…')] + [(year, year) for year in reversed(range(1844, timezone.now().year + 2))]
        months = [
            (0, 'Select a month…'),
            (1, 'January'),
            (2, 'February'),
            (3, 'March'),
            (4, 'April'),
            (5, 'May'),
            (6, 'June'),
            (7, 'July'),
            (8, 'August'),
            (9, 'September'),
            (10, 'October'),
            (11, 'November'),
            (12, 'December'),
        ]
        days = [(0, 'Select a day…')] +  [(day, day) for day in range(1, 32)]
        widgets = [
            forms.Select(attrs={'class': 'required'}, choices=years),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=days),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.year, value.month, value.day]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [year, month, day]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        year, month, day = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)


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


class ContactInfoForm(BaseForm):
    first_name = forms.CharField(max_length=254, required=False)
    middle_name = forms.CharField(max_length=254,required=False)
    last_name = forms.CharField(max_length=254, required=False)
    email = forms.EmailField(max_length=254, label='Email address')
    role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        label=safe('Are you/is this person a…'),
        widget=CheckboxSelectMultiple(attrs={'class': 'checkbox'})
    )


class BasicOrganizationInfoForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'url',
            'email',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'founded',
            'media_url',
            'logo_url',
        ]
        labels = {
            'name': _('What is the name of your enterprise or project?'),
            'url': _('What is the URL of your enterprise or project?'),
            'email': _('What is the general contact email address for your enterprise or project?'),
            'socialnetworks': _('What are the social media handles of your enterprise or project?'),
            'address': _(safe('What is the physical address of the headquarters of your enterprise or project?<br/> Street')),
            'state': _('State or province'),
            'founded': _(safe('When was your enterprise or project founded? (Year required. <span class="required"> *</span>)')),
            'media_url': _('Paste a link to photos or any introductory video about your enterprise or project:'),
            'logo_url': _('Paste a link to the logo for your enterprise or project:'),
        }
        help_texts = {
        }
        widgets = {
            'url': URLInput(attrs={'placeholder': 'e.g., https://example.coop/'}),
            'founded': DateSelectorWidget(),
            'media_url': URLInput(attrs={'placeholder': 'e.g., https://www.youtube.com/watch?v=qcPUARqRsVM'}),
            'logo_url': URLInput(attrs={'placeholder': 'e.g., https://example.coop/logo.png'}),
        }


class CategoriesChallengesForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'legal_status',
            'stage',
            'challenges',
            'categories',
            'sectors',
        ]
        labels = {
            'legal_status': _('What is your status if you are a legally incorporated enterprise?'),
            'stage': _('At what stage in the development process is your enterprise or project?'),
            'challenges': _('What challenges are you facing with your project or enterprise?'),
            'categories': _('Which terms do you use to describe your project or enterprise?'),
            'sectors': _('In which industries or sectors do you operate?'),
        }
        widgets = {
            'legal_status': CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
            'stage': RadioSelect(attrs={'class': 'radio'}),
            'challenges': CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
            'categories': CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
            'sectors': CheckboxSelectMultiple(attrs={'class': 'checkbox'})
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
