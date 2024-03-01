from django.shortcuts import render

from projects.models import Project
from users.models import Profile


# Create your views here.

def index(request):
    projects = Project.objects.all()

    context = {'projects': projects}
    return render(request, 'blogwcss/index.html', context)


def indextest(request):
    return render(request, 'blogwcss/indextest.html')


