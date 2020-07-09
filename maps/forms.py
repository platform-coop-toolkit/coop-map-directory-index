from datetime import datetime
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.forms import PointField, OSMWidget
from django.forms import CharField, CheckboxSelectMultiple, IntegerField, ModelChoiceField, RadioSelect, Select, SelectMultiple, HiddenInput, \
    NumberInput, TextInput, formset_factory, inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.template.defaultfilters import safe
from django_countries.fields import CountryField
from accounts.models import Role, SocialNetwork, UserSocialNetwork
from mdi.models import Organization, Category, Language, OrganizationSocialNetwork, Stage, Tool, Type, Pricing, License, LegalStatus, Challenge


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


class IndividualProfileDeleteForm(BaseModelForm):
    class Meta:
        model = get_user_model()
        fields = ['has_profile']
        widgets = {'has_profile': HiddenInput}


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
        required=False,
        label=_('State or province'),
        help_text=_('Please enter full state or province name rather than an abbreviated form.')
    )
    country = CountryField(blank=False).formfield()

    class Meta:
        model = get_user_model()
        fields = [
            'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'address': _('Street address'),
            'postal_code': _('ZIP or postal code')
        }


class GeolocationForm(BaseForm):
    lng = forms.CharField(required=False, widget=HiddenInput())
    lat = forms.CharField(required=False, widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        self.lat = kwargs['initial']['lat']
        self.lng = kwargs['initial']['lat']
        super(GeolocationForm, self).__init__(*args, **kwargs)
        self.fields['lat'].value = self.lat
        self.fields['lng'].value = self.lng


class IndividualRolesForm(BaseForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        label=_('How would you describe yourself?'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
    )


class IndividualMoreAboutYouForm(BaseModelForm):
    member_of = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you are a currently a member of'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
    )

    founder_of = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you are a founder of'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
    )

    worked_with = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you have worked with'),
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
            'community_skills',
            'field_of_study',
            'affiliation',
            'affiliation_url'
        ]
        labels = {
            'services': _('Services you provide'),
            'community_skills': _('What community building skills do you have to offer?'),
            'field_of_study': _('What is your field of research?'),
            'affiliation': _('Are you affiliated with an organization or institution?'),
            'affiliation_url': _('What is the website address of your affiliated organization or institution?'),
        }
        widgets = {
            'services': SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        }
        help_texts = {
            'community_skills': _('Provide a short description.')
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
    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            self.label = kwargs['initial']['name']
            self.hint = kwargs['initial']['hint']
        elif 'instance' in kwargs:
            self.label = kwargs['instance'].socialnetwork.name
            self.hint = kwargs['instance'].socialnetwork.hint
        super(IndividualSocialNetworkForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'label'):
            self.fields['identifier'].label = self.label
        if hasattr(self, 'hint'):
            self.fields['identifier'].widget = TextInput(attrs={'placeholder': self.hint})

    class Meta:
        model = UserSocialNetwork
        fields = [
            'socialnetwork',
            'identifier',
        ]
        widgets = {
            'socialnetwork': HiddenInput()
        }


IndividualSocialNetworkFormSet = formset_factory(IndividualSocialNetworkForm, extra=0)

IndividualEditSocialNetworkFormSet = inlineformset_factory(get_user_model(), UserSocialNetwork, form=IndividualSocialNetworkForm, extra=len(SocialNetwork.objects.all()), max_num=len(SocialNetwork.objects.all()))


class IndividualBasicInfoUpdateForm(BaseModelForm):
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
    city = CharField(
        required=True,
        label=_('City or town')
    )
    state = CharField(
        required=False,
        label=_('State or province'),
        help_text=_('Please enter full state or province name rather than an abbreviated form.')
    )
    country = CountryField(blank=False).formfield()
    lng = forms.CharField(required=False, widget=HiddenInput(attrs={'id': 'id_geolocation-lng'}))
    lat = forms.CharField(required=False, widget=HiddenInput(attrs={'id': 'id_geolocation-lat'}))

    def __init__(self, *args, **kwargs):
        self.lat = kwargs['initial']['lat']
        self.lng = kwargs['initial']['lat']
        super(IndividualBasicInfoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['lat'].value = self.lat
        self.fields['lng'].value = self.lng

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'languages',
            'url',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'middle_name': _('Middle name'),
            'url': _('Website address'),
            'address': _('Street address'),
            'postal_code': _('ZIP or postal code')
        }


class IndividualOverviewUpdateForm(BaseModelForm):
    member_of = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you are a currently a member of'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )

    founder_of = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you are a founder of'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )

    worked_with = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        label=_('Cooperative(s) you have worked with'),
        required=False,
        widget=SelectMultiple(attrs={'size': 4, 'class': 'multiple'}),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )

    class Meta:
        model = get_user_model()
        fields = [
            'roles',
            'member_of',
            'founder_of',
            'worked_with',
            'services',
            'community_skills',
            'field_of_study',
            'affiliation',
            'affiliation_url',
            'bio',
            'projects'
        ]
        labels = {
            'roles': _('How would you describe yourself?'),
            'services': _('Services you provide'),
            'community_skills': _('What community building skills do you have to offer?'),
            'field_of_study': _('What is your field of research?'),
            'affiliation': _('Are you affiliated with an organization or institution?'),
            'affiliation_url': _('What is the website address of your affiliated organization or institution?'),
            'bio': _('Bio'),
            'projects': _('Projects'),
        }
        widgets = {
            'roles': CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'}),
            'services': SelectMultiple(attrs={'size': 4, 'class': 'multiple'})
        }
        help_texts = {
            'services': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
            'community_skills': _('Provide a short description.'),
            'bio': _('Share a bit about yourself.'),
            'projects': _('List any current or past projects you would like to share with others.')
        }


class OrganizationTypeForm(BaseForm):
    type = forms.ModelChoiceField(
        Type.objects.filter(name__in=[
            'Cooperative',
            'Potential cooperative',
            'Shared platform'
            # 'Supporting organization' TODO: Add flow for these.
        ]),
        empty_label=None,
        label=_('How would you describe your organization?'),
        required=True,
        initial=0,
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )


class OrganizationBasicInfoForm(BaseModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=True,
        label=_('Working languages'),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )

    year_founded = IntegerField(
        required=True,
        label=_('Year'),
        max_value=datetime.now().year,
        widget=NumberInput(attrs={'id': 'year_founded'})
    )

    month_founded = forms.ChoiceField(
        choices=[
            ('', _('Not sure')),
            ('01', _('January')),
            ('02', _('February')),
            ('03', _('March')),
            ('04', _('April')),
            ('05', _('May')),
            ('06', _('June')),
            ('07', _('July')),
            ('08', _('August')),
            ('09', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December'))
        ],
        required=False,
        widget=Select(attrs={'id': 'month_founded'}),
        label=_('Month')
    )

    day_founded = forms.ChoiceField(
        choices=[
            ('', _('Not sure')),
            ('01', '1'),
            ('02', '2'),
            ('03', '3'),
            ('04', '4'),
            ('05', '5'),
            ('06', '6'),
            ('07', '7'),
            ('08', '8'),
            ('09', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
            ('24', '24'),
            ('25', '25'),
            ('26', '26'),
            ('27', '27'),
            ('28', '28'),
            ('29', '29'),
            ('30', '30'),
            ('31', '31')
        ],
        required=False,
        label=_('Day'),
        widget=Select(attrs={'id': 'day_founded'})
    )

    class Meta:
        model = Organization
        fields = [
            'name',
            'languages',
            'year_founded',
            'month_founded',
            'day_founded',
            'founded',
            'founded_min_date',
            'founded_max_date',
            'url'
        ]
        labels = {
            'url': _('Website address')
        }
        widgets = {
            'founded': HiddenInput({'id': 'founded'}),
            'founded_min_date': HiddenInput(attrs={'id': 'founded_min_date'}),
            'founded_max_date': HiddenInput(attrs={'id': 'founded_max_date'})
        }

    def __init__(self, *args, **kwargs):
        self.type = kwargs['initial']['type']
        super(OrganizationBasicInfoForm, self).__init__(*args, **kwargs)
        if self.type.name == 'Cooperative':
            self.fields['name'].label = _('Name of cooperative')
        else:
            self.fields['year_founded'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        orgs = Organization.objects.filter(name__exact=name)
        if len(orgs) > 0:
            err = forms.ValidationError(
                _('An organization named <a href="/organizations/%(url)s">%(name)s</a> is already listed in the directory.'),
                code='invalid',
                params={
                    'url': orgs[0].id,
                    'name': name
                },
            )
            self.add_error('name', err)


class OrganizationContactInfoForm(BaseModelForm):
    city = CharField(
        required=True,
        label=_('City or town')
    )
    state = CharField(
        required=False,
        label=_('State or province'),
        help_text=_('Please enter full state or province name rather than an abbreviated form.')
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
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_('Co-op type'),
        help_text=_('Choose all that apply.'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'})
    )

    num_workers = IntegerField(
        required=True,
        label=_('Number of workers'),
        help_text=_('Please provide your best estimate.')
    )

    num_members = IntegerField(
        required=False,
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

    def __init__(self, *args, **kwargs):
        self.type = kwargs['initial']['type']
        super(OrganizationDetailedInfoForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(type=self.type)
        if self.type.name == 'Cooperative':
            self.fields['num_members'].required = True
            self.fields['categories'].required = True
        else:
            self.fields['num_workers'].required = False

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
        help_texts = {
            'sectors': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
        }


class OrganizationScopeAndImpactForm(BaseModelForm):
    geo_scope = forms.ChoiceField(
        choices=[
            ('', _('Not sure')), ('Local', 'Local'), ('Regional', 'Regional'), ('National', 'National'), ('International', 'International')
        ],
        required=False,
        label=_('Primary geographic scope'),
        help_text=_('Choose primary scope.'),
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )

    class Meta:
        model = Organization
        fields = [
            'geo_scope',
            'geo_scope_city',
            'geo_scope_region',
            'geo_scope_country',
            'impacted_exact_number'
        ]
        labels = {
            'geo_scope_city': _('City or town'),
            'geo_scope_region': _('State or province'),
            'geo_scope_country': _('Country'),
            'impacted_exact_number': _('Number of people your co-operative impacts (directly and indirectly)')
        }
        help_texts = {
            'impacted_exact_number': _('Include clients and users as well as their family members or others indirectly impacted by the work of your co-operative.')
        }


class OrganizationSocialNetworkForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            self.label = kwargs['initial']['name']
            self.hint = kwargs['initial']['hint']
        elif 'instance' in kwargs:
            self.label = kwargs['instance'].socialnetwork.name
            self.hint = kwargs['instance'].socialnetwork.hint
        super(OrganizationSocialNetworkForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'label'):
            self.fields['identifier'].label = self.label
        if hasattr(self, 'hint'):
            self.fields['identifier'].widget = TextInput(attrs={'placeholder': self.hint})

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

OrganizationEditSocialNetworkFormSet = inlineformset_factory(Organization, OrganizationSocialNetwork, form=OrganizationSocialNetworkForm, extra=len(SocialNetwork.objects.all()), max_num=len(SocialNetwork.objects.all()))


class OrganizationBasicInfoUpdateForm(BaseModelForm):
    type = forms.ModelChoiceField(
        Type.objects.filter(name__in=[
            'Cooperative',
            'Potential cooperative',
            'Shared platform'
            # 'Supporting organization' TODO: Add flow for these.
        ]),
        empty_label=None,
        label=_('How would you describe your organization?'),
        required=True,
        initial=0,
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )

    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=True,
        label=_('Working languages'),
        help_text=_('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.')
    )

    class Meta:
        model = Organization
        fields = [
            'type',
            'name',
            'languages',
            'url'
        ]
        labels = {
            'type': _('Organization type'),
            'url': _('Website address')
        }
        help_texts = {}


class OrganizationOverviewUpdateForm(BaseModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_('Co-op type'),
        help_text=_('Choose all that apply.'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'})
    )

    legal_status = forms.ModelMultipleChoiceField(
        queryset=LegalStatus.objects.filter(order__lt=9999),
        required=False,
        label=_('Legal status'),
        help_text=_('Choose all that apply.'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group radio'})
    )

    num_workers = IntegerField(
        required=True,
        label=_('Number of workers'),
        help_text=_('Please provide your best estimate.')
    )

    num_members = IntegerField(
        required=False,
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

    challenges = forms.ModelMultipleChoiceField(
        queryset=Challenge.objects.filter(order__lt=9999),
        required=False,
        label=_('Challenges'),
        help_text=_('Choose all that apply.'),
        widget=CheckboxSelectMultiple(attrs={'class': 'input-group checkbox'})
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

    year_founded = IntegerField(
        required=True,
        label=_('Year'),
        max_value=datetime.now().year,
        widget=NumberInput(attrs={'id': 'year_founded'})
    )

    month_founded = forms.ChoiceField(
        choices=[
            ('', _('Not sure')),
            ('01', _('January')),
            ('02', _('February')),
            ('03', _('March')),
            ('04', _('April')),
            ('05', _('May')),
            ('06', _('June')),
            ('07', _('July')),
            ('08', _('August')),
            ('09', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December'))
        ],
        required=False,
        widget=Select(attrs={'id': 'month_founded'}),
        label=_('Month')
    )

    day_founded = forms.ChoiceField(
        choices=[
            ('', _('Not sure')),
            ('01', '1'),
            ('02', '2'),
            ('03', '3'),
            ('04', '4'),
            ('05', '5'),
            ('06', '6'),
            ('07', '7'),
            ('08', '8'),
            ('09', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
            ('24', '24'),
            ('25', '25'),
            ('26', '26'),
            ('27', '27'),
            ('28', '28'),
            ('29', '29'),
            ('30', '30'),
            ('31', '31')
        ],
        required=False,
        label=_('Day'),
        widget=Select(attrs={'id': 'day_founded'})
    )

    geo_scope = forms.ChoiceField(
        choices=[
            ('', _('Not sure')), ('Local', 'Local'), ('Regional', 'Regional'), ('National', 'National'), ('International', 'International')
        ],
        required=False,
        label=_('Primary geographic scope'),
        help_text=_('Choose primary scope.'),
        widget=RadioSelect(attrs={'class': 'input-group radio', 'id': 'scope_and_impact-geo_scope'})
    )

    code_availability = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('Partially', 'Partially'), ('No', 'No')],
        required=False,
        label=_('Does your organization share your source code?'),
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )

    def __init__(self, *args, **kwargs):
        self.type = kwargs['initial']['type']
        super(OrganizationOverviewUpdateForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(type=self.type)
        if self.type.name == 'Cooperative':
            self.fields['num_members'].required = True
            self.fields['categories'].required = True
        else:
            self.fields['num_workers'].required = False

    class Meta:
        model = Organization
        fields = [
            'categories',
            'sectors',
            'num_workers',
            'num_members',
            'stage',
            'worker_distribution',
            'year_founded',
            'month_founded',
            'day_founded',
            'founded',
            'founded_min_date',
            'founded_max_date',
            'legal_status',
            'geo_scope',
            'geo_scope_city',
            'geo_scope_region',
            'geo_scope_country',
            'impacted_exact_number',
            'description',
            'challenges',
            'code_availability',
            'code_url'
        ]
        widgets = {
            'founded': HiddenInput({'id': 'founded'}),
            'founded_min_date': HiddenInput(attrs={'id': 'founded_min_date'}),
            'founded_max_date': HiddenInput(attrs={'id': 'founded_max_date'}),
            'geo_scope_city': TextInput(attrs={'id': 'id_scope_and_impact-geo_scope_city'}),
            'geo_scope_region': TextInput(attrs={'id': 'id_scope_and_impact-geo_scope_region'}),
            'geo_scope_country': Select(attrs={'id': 'id_scope_and_impact-geo_scope_country'}),
            'code_availability': RadioSelect(attrs={'class': 'input-group radio'})
        }
        labels = {
            'geo_scope_city': _('City or town'),
            'geo_scope_region': _('State or province'),
            'geo_scope_country': _('Country'),
            'impacted_exact_number': _('Number of people your co-operative impacts (directly and indirectly)'),
            'code_url': _('Link to source code'),
        }
        help_texts = {
            'sectors': _('Hold down the <kbd>ctrl</kbd> (Windows) or <kbd>command</kbd> (macOS) key to select multiple options.'),
            'impacted_exact_number': _('Include clients and users as well as their family members or others indirectly impacted by the work of your co-operative.'),
        }


class OrganizationContactUpdateForm(BaseModelForm):
    city = CharField(
        required=True,
        label=_('City or town')
    )
    state = CharField(
        required=False,
        label=_('State or province'),
        help_text=_('Please enter full state or province name rather than an abbreviated form.')
    )
    country = CountryField(blank=False).formfield()
    lng = forms.CharField(required=False, widget=HiddenInput(attrs={'id': 'id_geolocation-lng'}))
    lat = forms.CharField(required=False, widget=HiddenInput(attrs={'id': 'id_geolocation-lat'}))

    def __init__(self, *args, **kwargs):
        self.lat = kwargs['initial']['lat']
        self.lng = kwargs['initial']['lat']
        super(OrganizationContactUpdateForm, self).__init__(*args, **kwargs)
        self.fields['lat'].value = self.lat
        self.fields['lng'].value = self.lng

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


class ToolBasicInfoForm(BaseModelForm):
    class Meta:
        model = Tool
        fields = [
            'name',
            'niches',
            'description',
            'url'
        ]
        labels = {
            'name': _('Name of tool'),
            'niches': _('What is this tool used for?'),
            'description': _('Description of tool'),
            'url': _('URL of tool website')
        }
        help_texts = {
            'description': _('Max 270 characters.')
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        tools = Tool.objects.filter(name__exact=name)
        if len(tools) > 0:
            err = forms.ValidationError(
                _('A tool named <a href="https://tools.platform.coop/tools/%(slug)s">%(name)s</a> is already listed in the directory.'),
                code='invalid',
                params={
                    'slug': slugify(name),
                    'name': name
                },
            )
            self.add_error('name', err)


class ToolDetailedInfoForm(BaseModelForm):
    pricing = forms.ModelChoiceField(
        queryset=Pricing.objects.all(),
        empty_label=_('Not sure'),
        required=False,
        label=_('How much does this tool cost?'),
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )

    license = forms.ModelChoiceField(
        queryset=License.objects.all(),
        empty_label=_('Not sure'),
        required=False,
        label=_('Please choose a specific free / libre / open source license')
    )

    sector = forms.ChoiceField(
        choices=[('no', _('No')), ('yes', _('Yes'))],
        required=True,
        initial='no',
        label=_('Is this tool for a specific sector or sectors?'),
        widget=RadioSelect(attrs={'class': 'input-group radio'})
    )

    class Meta:
        model = Tool
        fields = [
            'pricing',
            'license_type',
            'license',
            'sector',
            'sectors',
            'languages_supported',
            'coop_made'
        ]
        labels = {
            'license_type': _('How is this tool licensed?'),
            'sectors': _('Please choose a sector or sectors:'),
            'languages_supported': _('What languages does this tool support?'),
            'coop_made': _('Was this tool created by a co-op?')
        }
        widgets = {
            'license_type': RadioSelect(attrs={'class': 'input-group radio'}),
            'coop_made': RadioSelect(attrs={'class': 'input-group radio'})
        }
