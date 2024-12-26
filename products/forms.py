from django import forms
from .models import Product


class CreateForm(forms.ModelForm):

    hashtags = forms.CharField(
        label="해시태그",
        widget=forms.TextInput(
            attrs={"placeholder": "스페이스바로 구분하여 해시태그 입력"}
        ),
        required=False,
    )

    class Meta:
        model = Product
        fields = ["name", "photo"]
        exclude = ["author", "hashtags"]
        labels = {
            "name": "카드 이름",
            "photo": "카드 사진",
        }
