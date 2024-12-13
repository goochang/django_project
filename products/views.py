from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from django.contrib.auth.decorators import login_required
from .forms import CreateForm


def detail_product(request, pk):
    product = Product.objects.get(pk=pk)
    print("product", product.photo)
    context = {
        "product": product,
    }
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
