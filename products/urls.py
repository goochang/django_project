"""
URL configuration for spartamarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from products import views as p_views

app_name = "products"

urlpatterns = [
    path("<int:pk>/", p_views.detail_product, name="detail_product"),
    path("<int:pk>/profile/", p_views.user_profile, name="user_profile"),
    path("<int:pk>/delete/", p_views.delete_product, name="delete_product"),
    path("<int:pk>/edit/", p_views.edit_product, name="edit_product"),
    path("create_product/", p_views.create_product, name="create_product"),
    path("wish/", p_views.wish_product, name="wish_product"),
    # path('create_product/', p_views.create_product, name="create_product"),
    # path('create_product_action/', p_views.create_product_action),
]
