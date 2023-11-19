from django.urls import path, include
from users.views import register_view, login_view, logout_view, profile_view, user_search, add_friend, remove_friend,accept_friend_request, reject_friend_request, friends_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('user_search/', user_search, name='user_search'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', remove_friend, name='remove_friend'),
    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends_list/<int:user_id>/', friends_list, name='friends_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
