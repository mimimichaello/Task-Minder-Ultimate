from django import forms
from projects.models import Project, Task, File
from users.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'responsible']
        labels = {
            'name': 'Короткое название задачи',
            'description': 'Описание',
            'responsible': 'Ответственный',
            'start_date': 'Начало работы',
            'end_date': 'Окончание работы',
        }

class TaskForm(forms.ModelForm):
    responsible = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('name', 'description', 'responsible', 'start_date', 'end_date', 'project', 'status')
        labels = {
            'name': 'Короткое название задачи',
            'description': 'Описание',
            'responsible': 'Ответственный',
            'start_date': 'Начало работы',
            'end_date': 'Окончание работы',
            'project': 'Проект',
            'status': 'Статус'
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
