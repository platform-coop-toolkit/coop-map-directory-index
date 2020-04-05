from django.contrib.auth import get_user_model
from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect, SelectMultiple
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from django.template.defaultfilters import safe
from accounts.models import Role
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


class RoleForm(BaseForm):
    name = forms.ModelMultipleChoiceField(
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
    class Meta:
        model = get_user_model()
        fields = [
            'bio',

        ]
        labels = {
            'bio': _('Share a bit about yourself'),
        }


class ContactInfoForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            # 'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code',
        ]
        labels = {
            'address': _('Street address'),
        }


class SocialNetworksForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'socialnetworks',
        ]
        labels = {
            'socialnetworks': _('socialnetworks'),
        }
