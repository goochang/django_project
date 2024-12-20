import os


def rename_imagefile_to_uid(instance, filename):
    upload_to = "images/profile/"
    ext = filename.split(".")[-1]

    if instance.user_id:
        uid = instance.user_id
        filename = "{}.{}".format(uid, ext)

    return os.path.join(upload_to, filename)
