from django.contrib import admin
from .models import *


# Register your models here.


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_author', 'is_customer')


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'username', 'email', 'created', 'id')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_grades', 'email', 'created', 'id')

    @admin.display(description='grades')
    def get_grades(self, obj):
        return "\n".join([p.name for p in obj.grade.all()])


class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'created', 'id')


"""
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'recipient', 'body', 'created', 'id')
"""


admin.site.register(CustomerUser, CustomerUserAdmin)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(CustomerProfile, CustomerProfileAdmin)

admin.site.register(Grade, GradeAdmin)

admin.site.register(Skill, SkillAdmin)

# admin.site.register(Message, MessageAdmin)
