from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect
from django.utils.translation import gettext_lazy as _
from accounts.models import User, Role


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
        label='How would you describe yourself?',
        widget=CheckboxSelectMultiple(attrs={'class': 'checkbox'})
    )


class BasicInfoForm(BaseModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'languages',
            # 'member_of',
            # 'founder_of',

        ]
        labels = {
            'first_name': _('First name'),
            'middle_name': _('Middle name'),
            'last_name': _('Last name'),
            'languages': _('Language(s) you speak'),
            # 'member_of': _('Name of your co-operative'),
            # 'founder_of': _('Name of co-ops you have founded'),
        }


class DetailedInfoForm(BaseModelForm):
    class Meta:
        model = User
        fields = [
            'bio',

        ]
        labels = {
            'bio': _('Share a bit about yourself'),
        }


class ContactInfoForm(BaseModelForm):
    class Meta:
        model = User
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
