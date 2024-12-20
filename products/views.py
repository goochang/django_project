from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Wish
from accounts.models import Account, Follow
from django.contrib.auth.decorators import login_required
from .forms import CreateForm
import json
import requests
from django.contrib.staticfiles import finders
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    author = get_object_or_404(Account, id=product.author_id)

    wishes = Wish.objects.filter(product=product, is_active=1)
    wishCnt = wishes.count()
    isWish = wishes.filter(user=request.user).count()

    isFollow = Follow.objects.filter(
        follow=product.author, user=request.user, is_active=1
    ).count()

    metadata = {
        "wishCnt": wishCnt,
        "isWish": isWish,
        "isFollow": isFollow,
    }

    product_name = product.name.split(" ")[0]
    file_path = finders.find("pokemon.json")

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                mapping = json.load(file)
            result = next((x for x in mapping if x["ko_name"] == product_name), None)
            if result:
                metadata["eng_name"] = result["eng_name"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading pokemon.json: {e}")
    else:
        logger.error("pokemon.json file not found.")

    context = {"product": product, "meta": metadata, "author": author}
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
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)

    if request.user.id != product.author_id:
        return redirect("index")

    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect("products:detail_product", pk=product.id)
    else:
        form = CreateForm(instance=product)

    context = {"form": form, "product": product}
    return render(request, "product/edit_product.html", context)


@login_required
def delete_product(request, pk):
    get_req = request.META.get("HTTP_X_REQUESTED_WITH")
    if request.method == "POST" and get_req == "XMLHttpRequest":
        product = Product.objects.get(pk=pk)  # AJAX에서 전달한 데이터
        if product and request.user.id == product.author_id:
            product.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Product delete",
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid product request"}
            )
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"})


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
