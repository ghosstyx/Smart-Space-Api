# from django.db.models.signals import post_save
# from django.contrib.auth import get_user_model
# from django.dispatch import receiver
# from user_profiles.models import Profile
#
#
# User = get_user_model()
#
#
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         instance.profile.save()
