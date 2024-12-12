from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product

def create_product(request):
	return render(request, "product/create_product.html")
def detail_product(request, pk):
	product = Product.objects.get(pk=pk)
	context = {
		"product": product,
	}
	return render(request, "product/detail_product.html", context)

def create_product_action(request):
	name = request.POST.get("name")
	price = request.POST.get("price")
	type = request.POST.get("type")

	product = Product()
	product.name = name
	product.price = price
	product.type = type
	product.save()		
	
	return redirect("detail_product", pk=product.id)