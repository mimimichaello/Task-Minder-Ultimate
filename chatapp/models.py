from django.db import models
from friendship.models import Friend
from autoslug import AutoSlugField
from users.models import User


class Room(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name', unique=True)
    members = models.ManyToManyField(User, related_name='room_members')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_creator')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_user_friend(self, user):
        return Friend.objects.are_friends(user, self)

    def add_member(self, user):
        if user.is_friend(self):
            self.members.add(user)
            return True
        return False

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


