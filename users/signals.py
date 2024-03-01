from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, CustomerProfile, OwnerProfile
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

"""def createdProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered')
    if created:
        user = instance
        if user.role == 'AUTHOR':
            Profile.objects.create(user=user,
                                   username=user.username,
                                   email=user.email,
                                   name=user.first_name).save()
            # profile.save()
            print('Author Profile Created correctly')


def deleteUser(sender, instance, **kwargs):
    user = instance.settings.AUTH_USER_MODEL
    user.delete()


post_save.connect(createdProfile, sender=settings.AUTH_USER_MODEL)

post_delete.connect(deleteUser, sender=Profile)"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # listens to user model, we want it to notice if a new user is added and create a profile
def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered')
    if created:
        user = instance

        if user.is_author:

            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=user.first_name,
            )
            profile.save()

        elif user.is_customer:

            customerprofile = CustomerProfile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=user.first_name,
            )
            customerprofile.save()

        # subject = 'Welcome to DevSearch'
        # message = "We are glad you are here!"

        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )


@receiver(post_save, sender=CustomerProfile)
def updateCustomer(sender, instance, created, **kwargs):
    customerprofile = instance
    user = customerprofile.user

    if not created:  # ensures consistency between user and profile (avoid recursion erorr)
        # User.objects.create(username=profile.username, email=profile.username, first_name=profile.first_name,
        # last_name=profile.last_name, is_participant=True) else:

        user.first_name = customerprofile.name
        user.username = customerprofile.username
        user.email = customerprofile.email
        user.is_customer = True
        user.save()


@receiver(post_save, sender=Profile)
def updateAuthor(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:  # ensures consistency between user and profile (avoid recursion erorr)
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.is_author = True
        user.save()


@receiver(post_delete, sender=Profile)  # listens to profile, we want it to notice if a profile is delete
# and delete the user too
def deleteAuthor(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


@receiver(post_delete, sender=CustomerProfile)  # listens to profile, we want it to notice if a profile is delete
# and delete the user too
def deleteCustomer(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


"""post_save.connect(createProfile, sender=settings.AUTH_USER_MODEL)"""
# post_save.connect(profileUpdated, sender=Profile) #you can do it like this if you don't want to use the decorator
# post_delete.connect(deleteUser, sender=Profile)
