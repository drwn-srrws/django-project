"""
URL configuration for project_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    # Список проектов
    path("", views.project_list, name="project_list"),
    # Детальная страница проекта
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    # Создание проекта
    path("projects/new/", views.create_project, name="create_project"),
    # Создание задачи
    path("projects/<int:project_id>/tasks/new/", views.create_task, name="create_task"),
    # Регистрация
    path("register/", views.register, name="register"),
    # Логин
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # Выход
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Профиль
    path("profile/", views.profile, name="profile"),
    # Создание проекта
    path("projects/new/", views.create_project, name="create_project"),
]
