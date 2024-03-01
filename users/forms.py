from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *

User = get_user_model()

"""class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
"""


class CustomRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'

        }

    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('customer_register')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})
            self.fields[name].help_text = None

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.username = user.username.lower()
        if commit:
            user.save()
        return user


class AuthorRegisterForm(UserCreationForm):
    """
    grade = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(AuthorRegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('author_register')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})
            self.fields[name].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_author = True
        user.username = user.username.lower()
        user.save()

        """profile = Profile.objects.create(user=user)
        profile.grade.add(*self.cleaned_data.get('grades'))"""
        return user


class AuthorGradesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('grade',)
        widgets = {
            'grade': forms.CheckboxSelectMultiple
        }


class AuthorProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'email', 'grade', 'location', 'short_intro', 'bio', 'profile_image',
                  'social_github', 'social_twitter', 'social_linkedin', 'social_youtube', 'social_website']
        widgets = {
            'grade': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(AuthorProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('users:author-account')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})


class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['username', 'name', 'email', 'adress', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('users:customer-account')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('users:author-account')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})

"""
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('users:author-account')
        self.helper.form_method = 'POST'

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})"""


