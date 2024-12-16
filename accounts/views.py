from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account
from products.models import Product
from .forms import SignupForm, SigninForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱
from django.contrib import messages


def index(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "index.html", context)


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get("user_id")
            password = form.cleaned_data.get("password")
            user = authenticate(user_id=user_id, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("index")
            else:
                messages.error(request, "잘못된 로그인 정보입니다.")
                return redirect(request.path)
        else:
            messages.error(request, "잘못된 로그인 정보입니다.")
            return redirect(request.path)
    else:
        form = SigninForm()
    context = {"form": form}
    return render(request, "account/signin.html", context)


def logout(request):
    auth_logout(request)
    return redirect("index")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
            print(user.photo)
            auth_login(request, user)
            return redirect("index")
        else:
            return render(request, "account/signup.html", {"form": form}, status=400)
    else:
        form = SignupForm()
        return render(request, "account/signup.html", {"form": form})


def mypage(request):
    user = request.user
    if user.is_authenticated:
        products = Product.objects.filter(author_id=user.id)
        context = {
            "user": user,
            "products": products,
        }
        return render(request, "account/mypage.html", context)
    else:
        redirect("index")
