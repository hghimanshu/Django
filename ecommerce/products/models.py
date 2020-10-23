from django.db import models
import os
import uuid
import random

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    return name, ext

def createUUIDdir(filename):
    fullPath = os.path.join("products",filename)
    print(fullPath)
    UUID_VALUE = uuid.uuid5(uuid.NAMESPACE_OID,fullPath)
    return UUID_VALUE


def upload_image_path(instance, filename):
    print(isinstance, filename)
    uuidDirValue = createUUIDdir(filename)
    new_filename = random.randint(1, 391010232929329)
    _, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{uuidDirValue}/{final_filename}".format(
        uuidDirValue=uuidDirValue,
        final_filename=final_filename
    )

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.title