from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .models import Project, Task
from .forms import ProjectForm, TaskForm, CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, "project_list.html", {"projects": projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "./templates/project_detail.html", {"project": project})


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
