from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = (
        ("Manager", "Manager"),
        ("Employee", "Employee"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Указываем unique related_name для полей
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # уникальное имя для реверсной связи
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # уникальное имя для реверсной связи
        blank=True,
        help_text="Specific permissions for this user.",
    )


# Комментарий
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


# Отчет
class Report(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.TextField()
    time_spent = models.PositiveIntegerField()  # Время в часах
    result = models.TextField()


# Задача
class Task(models.Model):
    STATUS_CHOICES = (
        ("In progress", "In progress"),
        ("Done", "Done"),
        ("Todo", "Todo"),
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="manager_tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    comments = models.ManyToManyField(Comment)


# Проект
class Project(models.Model):
    title = models.CharField(max_length=255)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="managed_projects"
    )
    users = models.ManyToManyField(User, related_name="projects")
    comments = models.ManyToManyField(Comment, blank=True)
    deadline = models.DateField()
    description = models.TextField(blank=True)
