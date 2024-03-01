from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.html import escape, mark_safe
from django.conf import settings

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# ROLES
OWNER = 1
CUSTOMER = 2
AUTHOR = 3
ROLE_CHOICES = (
    (OWNER, "Owner"),
    (CUSTOMER, 'Customer'),
    (AUTHOR, 'Project Author'),
)


class CustomerUser(AbstractUser):
    is_author = models.BooleanField("Projects Author", default=False)
    is_customer = models.BooleanField('Customer', default=False)
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add, creates automatic timestamp


class Grade(models.Model):

    GRADE_TYPE = (
        ('Frontend', 'Frontend Developer'),
        ('Backend', 'Backend Developer'),
        ('Fullstack', 'Fullstack Developer'),
        ('Designer', 'Web Designer'),
        ('Copywriter', 'Web Copywriter'),
    )
    name = models.CharField(max_length=50, choices=GRADE_TYPE)
    color = models.CharField(max_length=7, default='#DD7835')

    def __str__(self):
        return str(self.name)

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = ('<span class="tag tag--pill tag--main" style="color: %s, color: black; font-size: 10px; border: 1px '
                'solid red; padding: 5px; border-radius: 7px 7px" >%s</span>') % (color, name)
        return mark_safe(html)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    grade = models.ManyToManyField(Grade, related_name='author_grades')
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/authors_profiles', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']


class CustomerProfile(models.Model):
    # relation to user
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/customers_profile', default="profiles/user-default.png")
    adress = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']


# Owner Profile for more data for the owner
class OwnerProfile(models.Model):
    # relation to Owner
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner_first_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50, default='Adidas')
    company_description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.owner_first_name)

    class Meta:
        ordering = ['created']


class Skill(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created']


"""class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-is_read', '-created']"""














