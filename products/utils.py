import os
from django.apps import apps
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# from products.models import Product


class OverwriteStorage(FileSystemStorage):
    """
    file 같은 이름 존재시 overwrite
    """

    def get_available_name(self, name, max_length=20):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def rename_imagefile_to_pid(instance, filename):
    upload_to = "images/product/"
    ext = filename.split(".")[-1]

    Product = apps.get_model("products", "Product")  # '앱 이름', '모델 이름'

    if instance.id:
        uid = instance.id
    else:  # 새상품 등록
        uid = Product.objects.latest("id")
        uid = int(uid.id) + 1

    filename = "{}.{}".format(uid, ext)
    return os.path.join(upload_to, filename)
