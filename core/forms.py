from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )

    def clean_email(self):
        some_email = self.cleaned_data['email']
        if User.objects.filter(email=some_email).exists():
            raise ValidationError("This email is already registered")
        return some_email


class EmailForm(forms.Form):
    email = forms.EmailField()
