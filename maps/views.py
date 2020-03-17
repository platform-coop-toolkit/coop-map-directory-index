from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from accounts.models import User
from mdi.models import Organization


def index(request):
    template = loader.get_template('maps/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('maps/profile.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# Organization
def organization_detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    context = {
    }
    return render(request, 'maps/organization_detail.html', {'organization': organization})


# Individual
def individual_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
    }
    return render(request, 'maps/individual_detail.html', {'individual': user})


# Static pages
class PrivacyPolicyView(TemplateView):
    template_name = "maps/privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "maps/terms_of_service.html"


