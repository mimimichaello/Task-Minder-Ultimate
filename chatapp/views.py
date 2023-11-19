from django.shortcuts import render, redirect, get_object_or_404
from chatapp.models import Room, Message
from chatapp.forms import RoomForm
from django.contrib import messages
from users.models import User

def chat_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
        'title': 'Чат'
    }
    return render(request, 'chatapp/chat_list.html', context)

def chat_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room)[0:25]
    context = {
        'room': room,
        'messages': messages,
        'title': room.name
    }

    return render(request, 'chatapp/chat_room.html', context)

def create_room(request):
    my_friends = request.user.get_friends()
    rooms = Room.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            form.save_m2m()
            messages.success(request, 'Комната создана.')
            return redirect('chat_list')
        else:
            messages.error(request, 'Ошибка при создании комнаты. Пожалуйста, проверьте введенные данные.')
    else:
        form = RoomForm(initial={'creator': request.user})

    context = {
        'form': form,
        'my_friends': my_friends,
        'title': 'Создать комнату',
        'rooms': rooms,
    }

    return render(request, 'chatapp/create_room.html', context)

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user == room.creator:
        room.delete()

    return redirect("chat_list")
