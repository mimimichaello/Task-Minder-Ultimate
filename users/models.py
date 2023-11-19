from django.db import models
from django.contrib.auth.models import AbstractUser
from friendship.models import Friend, Follow, FriendshipRequest

class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', null=True, blank=True)

    def get_friends(self):
        return Friend.objects.friends(self)

    def get_friend_requests(self):
        return Friend.objects.unrejected_requests(user=self)

    def add_friend(self, to_user):
        Friend.objects.add_friend(self, to_user)

    def remove_friend(self, to_user):
        Friend.objects.remove_friend(self, to_user)

    def is_friend(self, other_user):
        return Friend.objects.are_friends(self, other_user)




