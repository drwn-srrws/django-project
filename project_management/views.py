from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .models import Project, Task, Comment, Report
from .forms import (
    ProjectForm,
    TaskForm,
    CustomUserCreationForm,
    CommentForm,
    ReportForm,
    EditProjectForm,
    EditTaskForm,
)
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def project_list(request):
    # Фильтрация проектов в зависимости от роли пользователя
    if request.user.role == "manager" or request.user.is_staff:
        projects = Project.objects.all()  # Менеджеры и staff видят все проекты
    else:
        projects = Project.objects.filter(
            users=request.user
        )  # Пользователи видят только те проекты, в которых состоят

    return render(request, "project_list.html", {"projects": projects})


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail.html", pk=project_id)
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form, "project": project})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически залогиниваем пользователя
            return redirect("project_list")  # Перенаправляем на список проектов
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def create_project(request):
    # Проверяем, является ли пользователь менеджером
    if request.user.role != "Manager":
        return redirect(
            "project_list"
        )  # Перенаправляем на список проектов, если это не менеджер

    if request.method == "POST":
        form = ProjectForm(
            request.POST, user=request.user
        )  # Передаем текущего пользователя в форму
        if form.is_valid():
            # Сохраняем проект без менеджера
            project = form.save(commit=False)
            project.manager = (
                request.user
            )  # Устанавливаем менеджера проекта как текущего пользователя
            project.save()  # Сохраняем проект
            form.save_m2m()  # Сохраняем связи ManyToMany (пользователи и комментарии)
            return redirect(
                "project_list"
            )  # Перенаправляем на список проектов после успешного создания
    else:
        form = ProjectForm(user=request.user)  # Передаем текущего пользователя в форму

    return render(request, "projects/create_project.html", {"form": form})


# Обновленный проект
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.role == "Employee":
        tasks = project.tasks.filter(
            assigned=request.user
        )  # Отображаем только задачи, назначенные пользователю
    else:
        tasks = project.tasks.all()

    comments = project.comments.all()

    # Обработка комментария
    if request.method == "POST" and "comment_submit" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            project.comments.add(comment)
            return redirect("project_detail", project_id=project.id)

    else:
        comment_form = CommentForm()

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


# Добавление задачи
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.manager = request.user
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm(project=project)

    return render(
        request,
        "projects/add_task.html",
        {
            "form": form,
            "project": project,
        },
    )


# Детальная страница задачи
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(
        request,
        "projects/task_detail.html",
        {
            "task": task,
        },
    )


@login_required
def add_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Проверяем, назначен ли пользователь на эту задачу
    if task.assigned != request.user and request.user.role != "Manager":
        return redirect("task_detail", task_id=task.id)

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.task = task
            report.user = request.user
            report.save()
            return redirect("task_detail", task_id=task.id)
    else:
        form = ReportForm()

    return render(request, "projects/add_report.html", {"task": task, "form": form})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()  # Сохраняем проект с выбранными комментариями
            return redirect("project_detail", project_id=project.id)
    else:
        form = EditProjectForm(instance=project)

    return render(
        request,
        "projects/edit_project.html",
        {"project": project, "project_form": form},
    )


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Сохраняем изменения в задаче
            return redirect("task_detail", task_id=task.id)
    else:
        form = EditTaskForm(instance=task)  # Загружаем текущую задачу в форму

    return render(request, "projects/edit_task.html", {"form": form, "task": task})


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.role == 'Manager':
        project.delete()
        return redirect('project_list')  # перенаправление на список проектов или другую страницу
    else:
        # если роль не менеджер, возвращаем ошибку или перенаправляем на главную
        return redirect('project_list')
    
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)  # Обновляем пароль, если он был изменен
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})
