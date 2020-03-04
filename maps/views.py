from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
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
