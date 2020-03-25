from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .forms import UserForm, RoleForm, OrganizationForm

from accounts.models import User
from mdi.models import Organization, Category, Sector, Type


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        user_form = UserForm()
        role_form = RoleForm()
        organization_form = OrganizationForm()

    return render(request, 'surveys/index.html', {
        'user_form': user_form,
        'role_form': role_form,
        'organization_form': organization_form,
    })
