from django.contrib.auth import get_user_model
from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect, SelectMultiple, HiddenInput, formset_factory
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from django.template.defaultfilters import safe
from accounts.models import Role, SocialNetwork, UserSocialNetwork
from mdi.models import Organization


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)


class BranchForm(forms.Form):
    type = forms.ChoiceField(
        choices=[('org', 'Organisation'), ('ind', 'Individual')],
        label='Are you creating a profile for an organisation, or for an individual?',
        widget=RadioSelect(attrs={'class': 'radio'}),
    )


class RolesForm(BaseForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        label=safe('How would you describe yourself?<br /><div class="space"></div><small>Choose all that apply</small>'),
        widget=CheckboxSelectMultiple(attrs={'class': 'checkbox'})
    )


class BasicInfoForm(BaseModelForm):
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
            'first_name',
            'middle_name',
            'last_name',
            'languages',
            'member_of',
            'founder_of',
        ]
        labels = {
            'first_name': _('First name'),
            'middle_name': _('Middle name'),
            'last_name': _('Last name'),
            'languages': _('Language(s) you speak'),
        }
        widgets = {
            'languages': SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
            'member_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
            'founder_of': autocomplete.ModelSelect2Multiple(url='organization-autocomplete'),
        }


class DetailedInfoForm(BaseModelForm):
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


class ContactInfoForm(BaseModelForm):
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


class UserSocialNetworkForm(BaseModelForm):
    class Meta:
        model = UserSocialNetwork
        fields = [
            'socialnetwork',
            'identifier',
        ]
        widgets = {
            'socialnetwork': HiddenInput(),
        }


UserSocialNetworkFormSet = formset_factory(UserSocialNetworkForm, extra=0)
