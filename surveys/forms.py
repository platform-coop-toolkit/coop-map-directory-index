from django.forms import ModelForm, TextInput, Textarea, RadioSelect, DateTimeInput
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from mdi.models import Organization


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'role'
        ]
        labels = {
            'role': _('Are you a…'),
        }
        widgets = {
            'role': RadioSelect()
        }


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'url',
            'email',
            'socialnetworks',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'founded',
        ]
        labels = {
            'name': _('What is the name of your enterprise or project?'),
            'url': _('What is the URL of your enterprise or project?'),
            'email': _('What is the general contact email address for your enterprise or project?'),
            'socialnetworks': _('What are the social media handles of your enterprise or project?'),
            'state': _('State or province'),
            'founded': _('When was your enterprise or project founded?')
        }
        help_texts = {
        }
        widgets = {
            'url': TextInput(attrs={'placeholder': 'e.g., https://example.coop/'}),
            'founded': DateTimeInput(format="%d/%m/%Y", attrs={'placeholder':"DD/MM/YY"})
        }



