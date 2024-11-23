from django.contrib import admin
from .models import User, Comment, Report, Task, Project
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelMultipleChoiceField, Textarea
from django.db.models import ManyToManyField
from django.db import models

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {'widget': admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)},
    }

# Регистрация кастомного класса администратора
admin.site.register(User, CustomUserAdmin)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Task)
admin.site.register(Project, ProjectAdmin)
