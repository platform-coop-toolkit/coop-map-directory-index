from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404, render
from .forms import IndividualForm, OrganizationForm, LegalStatusForm, StageForm, CategoryForm, SectorForm

from accounts.models import User
from mdi.models import Organization, Category, Sector, Type


class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render(self.request, 'surveys/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


FORMS = [
    ('individual', IndividualForm),
    ('organization', OrganizationForm),
]

TEMPLATES = {
    'individual': 'surveys/individual.html',
    'organization': 'surveys/index.html',
}


class SurveyWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

