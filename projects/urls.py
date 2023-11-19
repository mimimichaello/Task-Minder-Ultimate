from django.urls import path
from projects.views import project_view, single_project_view, create_project, edit_project, delete_project
from projects.views import create_task, edit_task, delete_task, search_tasks, project_detail, delete_file, index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('projects/', project_view, name='projects'),
    path('single_project/<int:project_id>/', single_project_view, name='single_project'),
    path('create_project/', create_project, name="create_project"),
    path('edit_project/<int:project_id>/', edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('create_task/', create_task, name='create_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('search_task/<int:project_id>/', search_tasks, name='search_tasks'),
    path('project_detail<int:project_id>/', project_detail, name='project_detail'),
    path('delete_file<int:file_id>/', delete_file, name='delete_file'),
    path('', index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

