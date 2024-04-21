import random
import string
from django.db import models
import uuid
from django.utils.crypto import get_random_string
import os
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


class TopBanner(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                           editable=False, null=False, blank=True)
