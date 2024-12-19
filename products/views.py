from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Account, Wish
from django.contrib.auth.decorators import login_required
from .forms import CreateForm
import json
import requests
from django.contrib.staticfiles import finders
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def detail_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        product = None

    if product is None:
        return redirect("index")

    try:
        author = Account.objects.get(pk=product.author_id)
    except Product.DoesNotExist:
        author = None
    if author is None:
        return redirect("index")

    metadata = {}
    wishes = Wish.objects.filter(product=product, is_active=1)
    try:
        isWish = Wish.objects.filter(
            product=product, user=request.user, is_active=1
        ).count()
        wishCnt = wishes.count()
    except:
        isWish = 0
        wishCnt = 0
    metadata["wishCnt"] = wishCnt
    metadata["isWish"] = isWish

    product_name = product.name.split(" ")[0]
    file_path = finders.find("pokemon.json")

    # 파일 열기
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            mapping = json.load(file)

        result = list(filter(lambda x: x["ko_name"] == product_name, mapping))

        if result:
            english_name = result[0]["eng_name"]
            metadata["eng_name"] = english_name

        context = {"product": product, "meta": metadata, "author": author}
        print(metadata)

    return render(request, "product/detail_product.html", context)


@login_required
def create_product(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print(product)
            product.author = request.user
            product.save()
            return redirect("products:detail_product", pk=product.id)
    else:
        form = CreateForm()

    context = {"form": form}
    return render(request, "product/create_product.html", context)


@login_required
def wish_product(request):
    get_req = request.META.get("HTTP_X_REQUESTED_WITH")
    if request.method == "POST" and get_req == "XMLHttpRequest":
        product_id = request.POST.get("product_id")  # AJAX에서 전달한 데이터
        if product_id:
            product = get_object_or_404(Product, id=product_id)

            # 사용자와 연관된 위시리스트에 추가
            wish, created = Wish.objects.get_or_create(
                user=request.user, product=product
            )
            print(product, wish, created)
            if created == False:
                wish.is_active = 0 if wish.is_active == 1 else 1
                wish.save()

            wishes = Wish.objects.filter(product=product, is_active=1)
            print(wishes)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Product added to wishlist",
                    "product": {"id": product.id},
                    "wish": {"isActive": wish.is_active},
                    "wishCnt": wishes.count(),
                }
            )
        else:
            return JsonResponse({"status": "error", "message": "Invalid product ID"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
