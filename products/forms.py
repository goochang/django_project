from django import forms
from .models import Product


class CreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["author"]
        labels = {
            "name": "카드 이름",
            "price": "가격",
            "type": "타입",
            "photo": "카드 사진",
        }

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if Account.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Username already exists.")
    #     return username
