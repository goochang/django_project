from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Wish, HashTag
from accounts.models import Account, Follow
from django.contrib.auth.decorators import login_required
from .forms import CreateForm
import json
import requests
from django.contrib.staticfiles import finders
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)


def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    author = get_object_or_404(Account, id=product.author_id)

    wishes = Wish.objects.filter(product=product, is_active=1)
    wishCnt = wishes.count()

    user = request.user
    if user.id:
        isWish = wishes.filter(user=request.user).count()

        isFollow = Follow.objects.filter(
            follow=product.author, user=request.user, is_active=1
        ).count()
    else:
        isWish = 0
        isFollow = 0

    # 조회수
    product.viewCnt += 1
    product.save()

    hashtags = product.hashtags.all()

    metadata = {
        "wishCnt": wishCnt,
        "viewCnt": product.viewCnt,
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

    poke_type = [
        "bug",
        "dark",
        "dragon",
        "eletric",
        "fairy",
        "fighting",
        "fire",
        "flying",
        "ghost",
        "grass",
        "ground",
        "ice",
        "normal",
        "poison",
        "psychic",
        "rock",
        "steel",
        "water",
    ]

    context = {
        "product": product,
        "meta": metadata,
        "author": author,
        "hashtags": hashtags,
        "poke_type": poke_type,
    }
    return render(request, "product/detail_product.html", context)


@login_required
def create_product(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        print(request.POST.get("hashtags").split("|"))
        if form.is_valid() and request.user:
            product = form.save(commit=False)
            print(product)
            product.author = request.user
            product.save()

            hashtags = request.POST.get("hashtags")
            if hashtags != "":
                for hash_text in hashtags.split("|"):
                    hashtag, created = HashTag.objects.get_or_create(name=hash_text)
                    product.hashtags.add(hashtag)

            return redirect("products:detail_product", pk=product.id)

        print(form.errors.items())
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

            hashtags = product.hashtags.all()
            print(hashtags)
            new_hashtags = request.POST.get("hashtags").split("|")

            for hashtag in hashtags:
                # 기존 해시태그 중 요청 해시태그에 있는 경우 요청 값 제거
                if hashtag.name in new_hashtags:
                    print("in", hashtag)
                    new_hashtags.remove(hashtag.name)
                else:  # 기존 해시태그 중 요청 해시태그에 없는 경우 삭제
                    print("delete", hashtag)
                    product.hashtags.remove(hashtag)

            # hashtags = request.POST.get("hashtags")
            print(new_hashtags)
            if len(new_hashtags) > 0 and new_hashtags[0] != "":
                for hash_text in new_hashtags:
                    hashtag, created = HashTag.objects.get_or_create(name=hash_text)
                    product.hashtags.add(hashtag)
            return redirect("products:detail_product", pk=product.id)

        print(form.errors.items())
    else:
        form = CreateForm(instance=product)
    hashtags = product.hashtags.all()
    hashtags_txt = "|".join([hashtag.name for hashtag in hashtags])

    context = {
        "form": form,
        "product": product,
        "hashtags": hashtags,
        "hashtags_txt": hashtags_txt,
    }
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


def user_profile(request, pk):
    product = get_object_or_404(Product, pk=pk)
    author = get_object_or_404(Account, id=product.author_id)

    if product and author:
        products = Product.objects.filter(author_id=author.id)
        product_cnt = len(products)

        Follows = Follow.objects.filter(user=author, is_active=1)
        Followings = Follow.objects.filter(follow=author, is_active=1)
        isFollow = Follow.objects.filter(
            follow=author, user=request.user, is_active=1
        ).count()

        meta = {
            "product_cnt": product_cnt,
            "follow_cnt": Follows.count(),
            "following_cnt": Followings.count(),
            "isFollow": isFollow,
        }
        context = {
            "author": author,
            "products": products,
            "meta": meta,
        }
        print(meta)
        return render(request, "account/mypage.html", context)
    else:
        redirect("index")


def search(request):
    sort = request.GET.get("sort")
    products = Product.objects.distinct().order_by("-created_at").all()
    if sort == "hot":
        products = products.annotate(wish_count=Count("product")).order_by(
            "-wish_count", "-created_at"
        )

    # queryset = Product.objects.all()

    # 요청에서 검색 파라미터 가져오기
    search = request.GET.get("search", None)
    print(search)

    # 검색 필터링 적용 (title, author)
    if search:
        products = products.filter(
            Q(name__icontains=search)
            | Q(author__username__icontains=search)
            | Q(hashtags__name__icontains=search)
        )

    context = {
        "products": products,
        "sort": sort,
        "search": search,
    }
    return render(request, "product/search_product.html", context)
