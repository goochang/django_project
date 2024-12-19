from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account, Follow
from products.models import Product
from .forms import SignupForm, SigninForm, EditAccountForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404  # 추가
from django.http import JsonResponse


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
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
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


def edit_account(request):
    _user = request.user
    context = {
        "user": _user,
    }
    if _user.is_authenticated and request.method == "POST":
        form = EditAccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST.get("username")
            user.introduce = request.POST.get("introduce")
            if request.FILES.get("photo") is None:
                user.save()
            else:
                user.save(isFile=True)

            return redirect("accounts:mypage")
        else:
            return render(request, "account/edit_account.html", context, status=400)
    else:
        if _user.is_authenticated:
            return render(request, "account/edit_account.html", context)
        else:
            redirect("index")


@login_required
def follow(request):
    get_req = request.META.get("HTTP_X_REQUESTED_WITH")
    if request.method == "POST" and get_req == "XMLHttpRequest":
        user = request.user
        if user:
            # 사용자와 연관된 위시리스트에 추가
            follow, created = Follow.objects.get_or_create(user=user)
            print(user, follow, created)
            if created == False:
                follow.is_active = 0 if follow.is_active == 1 else 1
                follow.save()
            exit()

            follows = Follow.objects.filter(user=user, follow=follow, is_active=1)
            print(follows)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Account added to followlist",
                    "user": {"id": user.id},
                    "follow": {"isActive": follow.is_active},
                    "followCnt": follows.count(),
                }
            )
        else:
            return JsonResponse({"status": "error", "message": "Invalid account ID"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
