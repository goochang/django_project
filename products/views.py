from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from django.contrib.auth.decorators import login_required
from .forms import CreateForm
import json
import requests
from django.contrib.staticfiles import finders
from django.conf import settings


def detail_product(request, pk):
    product = Product.objects.get(pk=pk)
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

            # url = f"https://pokeapi.co/api/v2/pokemon/{english_name}"
            # response = requests.get(url)

            # if response.status_code == 200:
            #     data = response.json()
            #     metadata["poke_id"] = data["id"]
            #     metadata["weight"] = data["weight"]
            #     metadata["height"] = data["height"]

            #     # 포켓몬 타입
            #     poke_type = [_type["type"]["name"] for _type in data["types"]]

            #     metadata["poke_types"] = poke_type
            #     if len(poke_type):
            #         metadata["main_type"] = poke_type[0]

            #     # 포켓몬 특성
            #     for i in range(0, len(data["abilities"])):
            #         ability = data["abilities"][i]["ability"]
            #         url = ability["url"]
            #         response = requests.get(url)

            #         metadata["ability" + str(i + 1)] = url
            #     print(metadata)

        context = {"product": product, "meta": metadata}

    return render(request, "product/detail_product.html", context)


@login_required
def create_product(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES["photo"])
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
