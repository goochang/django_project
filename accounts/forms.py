from django import forms
from .models import Account

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
