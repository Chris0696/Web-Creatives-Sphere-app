from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room, Message


@login_required(login_url='users:login')
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chatrooms/rooms.html', {'rooms': rooms})


@login_required(login_url='users:login')
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'chatrooms/room.html', {'room': room, 'messages': messages})
