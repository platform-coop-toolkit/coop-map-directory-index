from django_registration.forms import RegistrationFormTermsOfService
from accounts.models import User


class UserRegistrationForm(RegistrationFormTermsOfService):
    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
