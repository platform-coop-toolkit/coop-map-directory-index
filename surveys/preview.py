from django.http import HttpResponseRedirect
from formtools.preview import FormPreview


class IndividualFormPreview(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/form/success')


class OrganizationFormPreview(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/form/success')


class SocialNetworksFormPreview(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/form/success')
