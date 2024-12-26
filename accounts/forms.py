from django import forms
from .models import Account
from django.contrib.auth.forms import UsernameField


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ["user_id", "username", "password", "photo"]

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")
        if Account.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError("이미 사용중인 아이디 입니다.")
        return user_id

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용중인 닉네임 입니다.")
        return username


class SigninForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["user_id", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # 콜론 제거

    user_id = forms.CharField(
        label="",
        strip=False,
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "아이디를 입력해주세요"},
        ),
        error_messages={"required": "아이디를 입력해주세요"},
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "비밀번호를 입력해주세요",
            }
        ),
        error_messages={"required": "비밀번호를 입력해주세요"},
    )

    error_messages = {
        "invalid_login": "올바른 사용자 이름과 비밀번호를 입력하십시오. 두 필드 모두 대소문자를 구분할 수 있습니다.",
        "inactive": "활성화되지 않은 사용자입니다.",
    }


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["photo", "username", "introduce"]
