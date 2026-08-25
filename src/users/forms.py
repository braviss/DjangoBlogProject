from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('First name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter first name'),
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('Last name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter last name'),
            'class': 'form-control'
        })
    )

    def save(self, request):
        user = super().save(request)
        user.last_name = self.cleaned_data.get('last_name', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.save()
        return user