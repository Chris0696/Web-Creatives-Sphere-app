from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from ..decorators import author_required
from ..forms import AuthorGradesForm, AuthorRegisterForm, AuthorProfileForm, SkillForm
from ..models import Profile

User = get_user_model()


class RegisterAuthor(CreateView):
    model = User
    form_class = AuthorRegisterForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'author'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Author created successfully!')
        login(self.request, user)
        return redirect('users:profiles')


@login_required(login_url='users:login')
def authorAccount(request):
    profile = request.user.profile

    Skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'Skills': Skills, 'projects': projects}

    return render(request, 'users/author_account.html', context)


class AuthorGrades(UpdateView):
    model = User
    form_class = AuthorGradesForm
    template_name = 'users/grades.html'
    success_url = reverse_lazy('users:profiles')

    def get_object(self):
        return self.request.user.author

    def form_valid(self, form):
        messages.success(self.request, 'Gardes updated with success!')
        return super().form_valid(form)


"""@method_decorator([login_required, author_required], name='dispatch')
class EditAuthorAccount(UpdateView):
    model = Profile
    form_class = AuthorProfileForm
    template_name = 'users/author_profile_form.html'
    success_url = reverse_lazy('users:edit-account')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Account updated with success!')
        return super().form_valid(form)"""


@login_required(login_url='users:login')
@author_required
def EditAuthorAccount(request):
    profile = request.user.profile
    form = AuthorProfileForm(instance=profile)

    if request.method == 'POST':
        form = AuthorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('author-account')

    context = {'form': form}
    return render(request, 'users/author_profile_form.html', context)


@login_required(login_url='users:login')
@author_required
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('author-account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='users:login')
@author_required
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, 'Skill was udpated successfully!')
            return redirect('author-account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('users:author-account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)




"""@login_required(login_url='users:login')
def inbox(request):
    profile = request.user.profile

    messageRequests = profile.messages.all()

    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}

    return render(request, 'users/inbox.html', context)"""
