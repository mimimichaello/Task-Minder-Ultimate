from django.db import models
from django.utils import timezone
from users.models import User

class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_responsible')

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('В работе', 'В работе'),
        ('Выполнено', 'Выполнено'),
        ('Просрочено', 'Просрочено')
    ]

    name = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_responsible')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В работе')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def is_overdue(self):
        return self.end_date < timezone.now().date()

    def overdue_days(self):
        if self.is_overdue():
            return (timezone.now().date() - self.end_date).days
        return 0

    def __str__(self):
        return self.name

class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/')

    def __str__(self):
        return f"{self.project.name} - {self.file.name}"
