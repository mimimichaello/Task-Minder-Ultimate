from django import forms
from chatapp.models import Room
from users.models import User
from django.forms import CheckboxSelectMultiple

class RoomForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-rounded'}))
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Room
        fields = ['name', 'members', 'creator']
        widgets = {
            'creator': forms.HiddenInput(),
        }
