from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from friendship.models import FriendshipRequest, Friend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from users.models import User
from django.core.cache import cache


"""SIGN_UP"""
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались')
                return redirect('profile')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
                print(f"Authentication failed for username: {username}")
                print(f"User object: {user}")
                print(f"Form errors: {form.errors}")
    else:
        form = UserLoginForm()
    context = {
        'title': 'Аутентификация',
        'form': form
    }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли.')
    return redirect('login')

"""PROFILE"""

def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user, files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    friend_requests = Friend.objects.unrejected_requests(request.user)
    friends = Friend.objects.friends(request.user)

    context = {
        'title': 'Профиль',
        'form': form,
        'friend_requests': friend_requests,
        'friends': friends,
    }
    return render(request, 'users/profile.html', context)

"""USER_SEARCH"""

@login_required
def user_search(request):
    search_query = request.GET.get('search_query', '')
    found_user = None
    user_data = None

    if search_query:
        found_user = User.objects.filter(
            Q(username__iexact=search_query) |
            Q(email__iexact=search_query)
        ).first()

        if found_user:
            user_data = {
                'user_id': found_user.id,
                'username': found_user.username,
                'first_name': found_user.first_name,
                'last_name': found_user.last_name,
                'email': found_user.email,
                'image': found_user.image
            }

    context = {
        'search_query': search_query,
        'found_user': found_user,
        'user_data': user_data,
        'title': 'Поиск'
    }
    return render(request, 'users/user_search.html', context)

"""FRIENDSHIP"""

@login_required
def add_friend(request, user_id):
    to_user = User.objects.get(id=user_id)
    existing_request = FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user)
    if existing_request.exists():
        messages.warning(request, f'Запрос в друзья {to_user.username} уже был отправлен.')
    else:
        FriendshipRequest.objects.create(from_user=request.user, to_user=to_user)
        cache.delete(f'friend_requests:{to_user.id}')
        messages.success(request, f'Запрос в друзья отправлен {to_user.username}.')

    return redirect('profile')




@login_required
def accept_friend_request(request, request_id):
    friendship_request = FriendshipRequest.objects.get(id=request_id)
    friendship_request.accept()
    messages.success(request, f'Вы приняли запрос на дружбу от пользователя {friendship_request.from_user.username}')
    return redirect('profile')

@login_required
def reject_friend_request(request, request_id):
    friendship_request = FriendshipRequest.objects.get(id=request_id)
    friendship_request.reject()
    messages.success(request, f'Вы отклонили запрос на дружбу от пользователя {friendship_request.from_user.username}')
    friendship_request.delete()
    return redirect('profile')

@login_required
def remove_friend(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    Friend.objects.remove_friend(from_user, to_user)
    cache.delete(f'friends:{from_user.id}')
    cache.delete(f'friends:{to_user.id}')
    messages.success(request, f'Пользователь {to_user.username} удален' )
    return redirect('profile')

@login_required
def friends_list(request, user_id):
    user = User.objects.get(id=user_id)
    friend_requests = FriendshipRequest.objects.requests(user)
    friends = Friend.objects.friends(user)
    context = {
        'friends': friends,
        'friend_requests': friend_requests,
    }

    return render(request, 'users/profile.html', context)





