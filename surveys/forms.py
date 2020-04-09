from django import forms
from django.forms import RadioSelect, CheckboxSelectMultiple, DateTimeInput, HiddenInput, URLInput, formset_factory
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import safe
from accounts.models import User, Role
from mdi.models import Organization, OrganizationSocialNetwork, Sector, SocialNetwork


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)


class BaseModelForm(forms.ModelForm):
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
            'founded': _('When was your enterprise or project founded?'),
            'media_url': _('Paste a link to photos or any introductory video about your enterprise or project:'),
            'logo_url': _('Paste a link to the logo for your enterprise or project:'),
        }
        help_texts = {
        }
        widgets = {
            'url': URLInput(attrs={'placeholder': 'e.g., https://example.coop/'}),
            'founded': DateTimeInput(format="%d/%m/%Y", attrs={'placeholder': "DD/MM/YY"}),
            'media_url': URLInput(attrs={'placeholder': 'e.g., https://www.youtube.com/watch?v=qcPUARqRsVM'}),
            'logo_url': URLInput(attrs={'placeholder': 'e.g., https://example.coop/logo.png'}),
        }


class SocialNetworksForm(BaseModelForm):
    class Meta:
        model = SocialNetwork
        fields = [
            'name',
            'description',
        ]


class LegalStatusForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'legal_status',
        ]
        labels = {
            'legal_status': _('What is your status if you are a legally incorporated enterprise?'),
        }
        widgets = {
            'legal_status': CheckboxSelectMultiple(attrs={'class': 'checkbox'})
        }


class StageForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'stage',
        ]
        labels = {
            'stage': _('At what stage in the development process is your enterprise or project?'),
        }
        widgets = {
            'stage': RadioSelect(attrs={'class': 'radio'})
        }


class CategoryForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'categories',
        ]
        labels = {
            'categories': _('Which terms do you use to describe your project or enterprise?'),
        }
        widgets = {
            'categories': CheckboxSelectMultiple(attrs={'class': 'checkbox'})
        }


class SectorForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = [
            'sectors',
        ]
        labels = {
            'sectors': _('In which industries or sectors do you operate?'),
        }
        widgets = {
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
