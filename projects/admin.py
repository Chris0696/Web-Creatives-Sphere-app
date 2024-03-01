from django.contrib import admin
from .models import *

# Register your models here.


class AdminProject(admin.ModelAdmin):

    list_display = ('title', 'demo_link', 'source_link', 'created', 'id')


class AdminReview(admin.ModelAdmin):
    list_display = ('project', 'body', 'value', 'created', 'id')


class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'created', 'id')


admin.site.register(Project, AdminProject)


admin.site.register(Review, AdminReview)

admin.site.register(Tag, AdminTag)


