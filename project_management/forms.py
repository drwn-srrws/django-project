from django import forms
from .models import Project, Task, Report, User, Comment
from django.contrib.auth.forms import UserCreationForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "manager", "users", "deadline"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned", "status"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["task", "progress", "time_spent", "result"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "Employee"  # Устанавливаем роль по умолчанию как 'Employee'
        if commit:
            user.save()
        return user


class ProjectForm(forms.ModelForm):
    comments = forms.ModelMultipleChoiceField(
        queryset=Comment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # Поле для выбора пользователей, работающих над проектом
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(
            role="Staff"
        ),  # Фильтруем пользователей по роли, исключая staff
        widget=forms.SelectMultiple,  # Используем мультиселект
        required=False,
    )

    class Meta:
        model = Project
        fields = ["title", "manager", "users", "comments", "deadline", "description"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Получаем текущего пользователя
        super(ProjectForm, self).__init__(*args, **kwargs)

        # Фильтруем менеджеров, исключая текущего пользователя
        if "manager" in self.fields and self.user:
            self.fields["manager"].queryset = self.fields["manager"].queryset.filter(
                id=self.user.id
            )

        # Фильтруем пользователей (кроме staff)
        if "users" in self.fields:
            self.fields["users"].queryset = User.objects.exclude(role="Staff")

    def clean_manager(self):
        manager = self.cleaned_data.get("manager")
        if manager and manager.role != "Manager":
            raise forms.ValidationError("You can only create projects as a manager.")
        return manager
