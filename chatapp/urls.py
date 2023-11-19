from django.urls import path
from chatapp.views import chat_list, chat_room, create_room, delete_room

urlpatterns = [
    path('chat/', chat_list, name='chat_list'),
    path('chat_room/<int:room_id>/', chat_room, name='chat_room'),
    path('create_room/', create_room, name='create_room'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room'),
]
