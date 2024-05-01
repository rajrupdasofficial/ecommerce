import random
import string
from django.db import models
import uuid
from django.utils.crypto import get_random_string
import os
from django.conf import settings
from taggit.managers import TaggableManager
# Create your models here.


def random_uuid():
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def random_string_generator(size=43, char=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def random_id_generator(size=15, char=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def thumbnail_upload_location(instance, filename):
    random_chars = get_random_string(22)
    image_file = random_chars
    random_image_name = get_random_string(27)
    _, file_extension = os.path.splitext(filename)
    image_name = f"{random_image_name}{file_extension}"
    return os.path.join(random_uuid(), image_file, image_name)


"""
Sliders
"""
# sliderclass


class Sliders(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    slider_images = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sliders ready with id - {self.uid}"

    class Meta:
        verbose_name_plural = "Sliders"


"""
Top banner model where banner based posts will be done
"""


class TopBanner(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    topimage = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    description = models.TextField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Topbanner created with id - {self.uid}"

    class Meta:
        verbose_name_plural = "TopBanner"


"""
Ads banner
"""


class Promotebanner(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,
                           editable=False, null=False, blank=True)
    promoteimages = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    description = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Promotional banner created with id - {self.uid}"

    class Meta:
        verbose_name_plural = "AdsBanner"


"""primary category"""


class Category(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    categoryicon = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    heading = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    desciption = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Category name - {self.heading} and id - {self.uid}"

    class Meta:
        verbose_name_plural = "Category"


"""subcategory"""


class Subcategory(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    category_belongs_to = models.ForeignKey(
        Category, verbose_name="category", on_delete=models.CASCADE)
    subcategoryicon = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    heading = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    desciption = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subcategory created with name - |{self.heading}| and - id - {self.uid}"

    class Meta:
        verbose_name_plural = "Subcategory"


"""
product size section
"""


class ProductSize(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    product_size_define = TaggableManager(blank=True)
    heading = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    desciption = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product size defined as -|  {self.heading} | created with id - {self.uid}"

    class Meta:
        verbose_name_plural = "ProductSize"


"""
products addition section
"""


class Products(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    category_belongs_to = models.ForeignKey(
        Category, verbose_name="category", on_delete=models.CASCADE)
    subcategory_belongs_to = models.ForeignKey(
        Subcategory, verbose_name="subcategory", on_delete=models.CASCADE)
    productimage = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    choose_size = models.ForeignKey(
        ProductSize, on_delete=models.CASCADE, null=True, blank=True, default=None)
    heading = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    desciption = models.TextField(default=None, null=True, blank=True)
    pricing = models.CharField(
        max_length=50, default=None, blank=True, null=True)
    discount = models.CharField(
        max_length=50, default=None, blank=True, null=True)
    quantity = models.BigIntegerField(default=None, blank=True, null=True)
    tags = TaggableManager(blank=True)
    who_purchased = models.CharField(
        max_length=300, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Products created with id - {self.uid}"

    class Meta:
        verbose_name_plural = "Products"


"""
CustomersProfile who is purchasing the products
"""


class CustomerProfile(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    email = models.EmailField(
        max_length=255, default=None, blank=True, null=True)
    username = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    phonenumber = models.BigIntegerField(default=None, blank=True, null=True)
    locality = models.CharField(
        max_length=120, default=None, blank=True, null=True)
    city = models.CharField(
        max_length=100, default=None, blank=True, null=True)
    zipcode = models.IntegerField()
    state = models.CharField(
        max_length=100, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CustomerProfile created with id - {self.uid}"

    class Meta:
        verbose_name_plural = "CustomerProfile"


"""

cart objects models
"""


class Cart(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart created with id - {self.uid}"

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

    class Meta:
        verbose_name_plural = "Cart"


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)

"""order placed model to track how much orders hasbeen placed"""


class OrderPlaced(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')
    cancel_product = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Oder Placed id {self.uid}"

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

    class Meta:
        verbose_name_plural = "OrderPlaced"


"""order history to check order history"""


class OrderHistory(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    total_productpurchased = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    purchased_productslist = models.ForeignKey(
        Products, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Oder History id {self.uid}"

    class Meta:
        verbose_name_plural = "OrderHistory"


""" Three cars """


class ThreeCards(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False, blank=True)
    threecarimages = models.ImageField(
        upload_to=thumbnail_upload_location, blank=True, null=True, default=None)
    heading = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cards with Name {self.heading}"

    class Meta:
        verbose_name_plural = "ThreeCards"
