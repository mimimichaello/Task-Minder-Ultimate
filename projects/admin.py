from django.contrib import admin
from projects.models import Project, Task, File

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'responsible')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'responsible', 'status')
    search_fields = ('name',)
    list_display_links = ('name',)

admin.site.register(File)
