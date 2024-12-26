from django import forms
from .models import Product


class CreateForm(forms.ModelForm):

    hashtags_input = forms.CharField(
        label="해시태그",
        widget=forms.TextInput(
            attrs={"placeholder": "스페이스바로 구분하여 해시태그 입력"}
        ),
    )

    class Meta:
        model = Product
        fields = ["name", "photo"]
        exclude = ["author"]
        labels = {
            "name": "카드 이름",
            "photo": "카드 사진",
        }

    def save(self, commit=True):
        product = super().save(commit=False)

        # 쉼표로 구분된 해시태그 입력 처리
        hashtags_data = self.cleaned_data["hashtags_input"]
        print(hashtags_data)

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if Account.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Username already exists.")
    #     return username
