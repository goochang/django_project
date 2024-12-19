from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Account
from django.contrib.auth.decorators import login_required
from .forms import CreateForm
import json
import requests
from django.contrib.staticfiles import finders
from django.conf import settings


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
