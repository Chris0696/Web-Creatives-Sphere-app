from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from .models import Project
from .forms import ProjectForm, ReviewForm
from users.decorators import author_required
from .utils import searchProjects


def index(request):
    return render(request, 'projects/index.html')


def projects(request):
    projects, search_query = searchProjects(request)

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    context = {'projects': projects, 'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.customerprofile
        review.save()

        var = projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('projects:project', pk=projectObj.id)

    context = {'project': projectObj, 'tags': tags, 'form': form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='users:login')
@author_required
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project was created successfully!')
            return redirect('author-account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='users:login')
@author_required
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project was update successfully!')
            return redirect('author-account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='users:login')
@author_required
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project was deleted successfully!')
        return redirect("author-account")
    context = {'object': project}
    return render(request, 'delete_template.html', context)
