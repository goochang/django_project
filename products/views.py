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

        # english_name = mapping.get(product.name, None)
        result = list(filter(lambda x: x["ko_name"] == product_name, mapping))

        if result:
            english_name = result[0]["eng_name"]
            metadata["eng_name"] = english_name

            url = f"https://pokeapi.co/api/v2/pokemon/{english_name}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                metadata["poke_id"] = data["id"]
                metadata["weight"] = data["weight"]
                metadata["height"] = data["height"]

                # POKETYPE = getattr(settings, "POKETYPE", None)
                # poke_type = [
                #     POKETYPE.get(_type["type"]["name"]) for _type in data["types"]
                # ]
                poke_type = [_type["type"]["name"] for _type in data["types"]]

                metadata["poke_types"] = poke_type
                if len(poke_type):
                    metadata["main_type"] = poke_type[0]

                abilities = []

                for ability in data["abilities"]:
                    url = ability["ability"]["url"]
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        flavor_text = [
                            flavor["flavor_text"]
                            for flavor in data["flavor_text_entries"]
                            if flavor["language"]["name"] == "ko"
                            and flavor["version_group"]["name"] == "x-y"
                        ]
                        flavor_name = [
                            poke_name["name"]
                            for poke_name in data["names"]
                            if poke_name["language"]["name"] == "ko"
                        ]
                        if len(flavor_text) and len(flavor_name):
                            abilities.append(
                                {"name": flavor_name[0], "content": flavor_text[0]}
                            )

                metadata["abilities"] = abilities
                print(metadata)

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
