from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.utils import timezone
from django.views.generic import CreateView, TemplateView
from ..models import *
from ..utils import searchProfiles
# from ..forms import MessageForm

User = get_user_model()


class SignUpView(TemplateView):
    template_name = 'users/signup_form.html'


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'users:profiles')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login_form.html')


def logoutUser(request):
    logout(request)
    # print('User was logged out!')
    messages.info(request, 'You have logged out')
    return redirect('users:login')


def AuthorsProfiles(request):
    profiles, search_query = searchProfiles(request)
    context = {'profiles': profiles, 'search_query': search_query}
    return render(request, 'users/authors_profiles.html', context)


def AuthorProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    '''print(profile.project)'''

    topskills = profile.skill_set.exclude(description__exact='')
    otherskills = profile.skill_set.filter(description='')

    context = {'profile': profile, 'topskills': topskills, 'otherskills': otherskills}
    return render(request, 'users/author_profile.html', context)


def CustomersProfiles(request):
    profiles = CustomerProfile.objects.all()

    context = {'profiles': profiles}
    return render(request, 'users/customers_profiles.html', context)


def customerProfile(request, pk):
    profile = CustomerProfile.objects.get(id=pk)
    print(profile.name)
    '''print(profile.project)'''

    context = {'profile': profile}
    return render(request, 'users/customer_profile.html', context)


"""@login_required(login_url='users:login')
def editAccount(request):
    context = {}
    return render(request, 'users/profile_form.html', context)"""

"""
@login_required(login_url='users:login')
def inbox(request):
    user = request.user
    messageRequests = user.messages.all()

    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}

    return render(request, 'users/inbox.html', context)


@login_required(login_url='users:login')
def viewMessage(request, pk):
    user = request.user
    message = user.messages.get(id=pk)
    if not message.is_read:
        messages.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


@login_required(login_url='users:login')
def sendMessage(request, pk):
    recipient = CustomerProfile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('users:user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
"""


"""
class SendMessage(CreateView):
    model = User
    form_class = MessageForm
    template_name = 'users/message_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'author'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Author created successfully!')
        login(self.request, user)
        return redirect('users:profiles')
"""