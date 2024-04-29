# from .models import CustomerProfile
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def post_save_create_profile(sender, instance, created, **kwargs):
#     if created:
#         CustomerProfile.objects.create(user=instance)
