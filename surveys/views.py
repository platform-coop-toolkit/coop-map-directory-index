from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactInfoForm, BasicOrganizationInfoForm, OrganizationSocialNetworkFormSet, LegalStatusForm, StageForm, CategoryForm, SectorForm

from accounts.models import User
from mdi.models import Organization, Category, Sector, Type, SocialNetwork


ECOSYSTEM_FORMS = [
    ('contact_info', ContactInfoForm),
    ('basic_organization_info', BasicOrganizationInfoForm),
    ('social_networks', OrganizationSocialNetworkFormSet),
]

ECOSYSTEM_TEMPLATES = {
    'contact_info': 'surveys/ecosystem_2020/contact_info.html',
    'basic_organization_info': 'surveys/ecosystem_2020/basic_organization_info.html',
    'social_networks': 'surveys/ecosystem_2020/social_networks.html',
}


class EcosystemWizard(SessionWizardView):
    def get_template_names(self):
        return [ECOSYSTEM_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        return context

    def get_form_initial(self, step):
        initial = []
        if step == 'social_networks':
            socialnetworks = SocialNetwork.objects.all()
            for index, sn in enumerate(socialnetworks):
                initial.append({
                    'socialnetwork' : sn,
                    'name': sn.name,
                    'hint' : sn.hint,
                })
            # print(initial)
        return self.initial_dict.get('social_networks', initial)

    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


def index(request):
    if request.method == 'POST':
        return redirect('ecosystem-2020')

    else:
        return render(request, 'surveys/ecosystem_2020/index.html')

