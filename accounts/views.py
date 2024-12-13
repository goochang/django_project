from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account
from products.models import Product
from .forms import SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱


def index(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "index.html", context)


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            print("is_valid", user)
            if user is not None:
                auth_login(request, user)
                return redirect("index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "account/signin.html", context)


def logout(request):
    auth_logout(request)
    return redirect("index")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
            auth_login(request, user)
            # account.set_password(form.cleaned_data["password"])  # 비밀번호 해싱
            return redirect("index")
        else:
            form = SignupForm()
            return render(request, "account/signup.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "account/signup.html", {"form": form})
