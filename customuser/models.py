from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    uid = models.CharField(default=uuid.uuid4, max_length=1000)
    email = models.EmailField(verbose_name="Email",
                              max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=10000)
    is_active = models.BooleanField(default=True)  # Add the is_active field
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
