from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Project, Task, File
from friendship.models import Friend
from django.contrib import messages
from users.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from projects.forms import ProjectForm, TaskForm, FileForm
from django.db.models import Q
from itertools import chain


def index(request):

    return render(request, 'projects/index.html', {'title': 'Начальная страница'})

def project_view(request):
    projects = Project.objects.filter(responsible=request.user)
    projects_with_task_count = projects.annotate(task_count=Count('tasks', filter=Q(tasks__status='В работе')))
    friend_users = Friend.objects.friends(request.user)
    friend_projects = Project.objects.filter(responsible__in=friend_users)
    projects_friend_with_task_count = friend_projects.annotate(task_count=Count('tasks'))
    users = User.objects.all()

    context = {
        'projects': projects_with_task_count,
        'users': users,
        'friend_projects': projects_friend_with_task_count,
        'title': 'Проекты',
    }
    return render(request, 'projects/projects.html', context)

def single_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    responsible_users = set()

    for task in tasks:
        responsible_users.add(task.responsible)

    friend_users = Friend.objects.friends(request.user)
    responsible_friends = [friend for friend in friend_users if friend in responsible_users]
    files = File.objects.filter(project=project)

    context = {
        'project': project,
        'title': project.name,
        'tasks': tasks,
        'users': responsible_friends,
        'files': files
    }

    return render(request, 'projects/single_project.html', context)

"""PROJECT"""

def create_project(request):
    your_friends = request.user.get_friends()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            messages.success(request, 'Проект создан.')
            return redirect('projects')
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'users': your_friends,
        'title': 'Создать проект'
    }

    your_friends.append(request.user)
    your_friends_queryset = User.objects.filter(id__in=[user.id for user in your_friends])
    form.fields['responsible'].queryset = your_friends_queryset

    return render(request, 'projects/create_project.html', context)

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.responsible:
        messages.warning(request, 'У вас нет прав для редактирования данного проекта.')
        return redirect('projects')

    your_friends = request.user.get_friends()
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект отредактирован.')
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'users': your_friends,
        'project': project,
        'title': project.name,
    }

    your_friends.append(request.user)
    your_friends_queryset = User.objects.filter(id__in=[user.id for user in your_friends])
    form.fields['responsible'].queryset = your_friends_queryset

    return render(request, 'projects/edit_project.html', context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.responsible:
        messages.warning(request, 'У вас нет прав для удаления данного проекта.')
        return redirect('projects')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удален.')
        return redirect('projects')

    context = {
        'project': project,
        'title': project.name,
    }

    return render(request, 'projects/edit_delete_project.html', context)

"""TASK"""

def create_task(request):
    your_friends = request.user.get_friends()
    status_choices = Task.STATUS_CHOICES
    friend_projects = Project.objects.filter(responsible__in=your_friends)
    your_projects = Project.objects.filter(responsible=request.user)
    all_projects = list(chain(your_projects, friend_projects))

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = Project.objects.get(pk=request.POST['project'])
            task.save()
            messages.success(request, f'Задача "{task.name}" создана')
            project_id = task.project.id
            return redirect('single_project', project_id=project_id)
    else:
        form = TaskForm()



    context = {
        'projects': all_projects,
        'form': form,
        'users': your_friends,
        'status_choices': status_choices,
        'title': 'Создать задачу'
    }
    your_friends.append(request.user)
    your_friends_queryset = User.objects.filter(id__in=[user.id for user in your_friends])
    form.fields['responsible'].queryset = your_friends_queryset

    return render(request, 'projects/create_task.html', context)

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    your_friends = request.user.get_friends()
    status_choices = Task.STATUS_CHOICES
    friend_projects = Project.objects.filter(responsible__in=your_friends)
    your_projects = Project.objects.filter(responsible=request.user)
    all_projects = list(chain(your_projects, friend_projects))

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Задача "{task.name}" отредактирована')
            project_id = task.project.id
            return redirect('single_project', project_id=project_id)
    else:
        form = TaskForm(instance=task)

    context = {
        'projects': all_projects,
        'form': form,
        'users': your_friends,
        'status_choices': status_choices,
        'task': task,
        'title': 'Редактировать'
    }
    your_friends.append(request.user)
    your_friends_queryset = User.objects.filter(id__in=[user.id for user in your_friends])
    form.fields['responsible'].queryset = your_friends_queryset

    return render(request, 'projects/edit_task.html', context)

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
            task.delete()
            messages.success(request, f'Задача удалена')
            project_id = task.project.id
            return redirect('single_project', project_id=project_id)

    context = {
        'task': task,
        'title': 'Удалить'
    }

    return render(request, 'projects/edit_task.html', context)

"""SEARCH"""

def search_tasks(request, project_id):
    query = request.GET.get('search_task', '')
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project=project, name__icontains=query)
    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'projects/single_project.html', context)


"""FILES"""

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    files = File.objects.filter(project=project)
    projects = Project.objects.all()
    tasks = Task.objects.filter(project=project)


    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = project
            file.save()
            return redirect('single_project', project_id=project_id)
    else:
        form = FileForm()

    context = {
        'project': project,
        'files': files,
        'form': form,
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'projects/single_project.html', context)

def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    projects = Project.objects.all()
    tasks = Task.objects.all()
    if request.method == 'POST':
        file.delete()
        project_id = file.project.id
        messages.success(request, f'Файл "{file.file.name}" удален')
        return redirect('single_project', project_id=file.project.id)

    context = {
        'tasks': tasks,
        'file': file,
        'projects': projects,
    }

    return render(request, 'projects/single_project.html', context)
