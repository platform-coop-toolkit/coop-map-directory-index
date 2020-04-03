from django import forms
from django.forms import TextInput, ModelForm, RadioSelect, CheckboxSelectMultiple, DateTimeInput, URLInput, modelformset_factory
from django.utils.translation import gettext_lazy as _
from accounts.models import User, Role
from mdi.models import Organization, Sector, SocialNetwork


class IndividualForm(forms.Form):
    first_name = forms.CharField(max_length=254, required=False)
    middle_name = forms.CharField(max_length=254,required=False)
    last_name = forms.CharField(max_length=254, required=False)
    email = forms.EmailField(max_length=254, label='Email address')
    role = forms.ChoiceField(choices=enumerate(Role.objects.all()), label='Are you/is this person a…', widget=RadioSelect(attrs={'class': 'radio'}))


class OrganizationForm(ModelForm):
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


class SocialNetworksForm(ModelForm):
    class Meta:
        model = SocialNetwork
        fields = [
            'name',
            'description',
        ]


class LegalStatusForm(ModelForm):
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


class StageForm(ModelForm):
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


class CategoryForm(ModelForm):
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


class SectorForm(ModelForm):
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
