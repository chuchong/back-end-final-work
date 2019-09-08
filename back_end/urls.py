"""back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from task.views import TaskListView, TaskCreateOrUpdateView, TaskDetailView, TaskDeleteView
from accounts.views import UserRegistrationView, UserLoginView
from back_end import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # as_view() 初始化view class,返回句柄
    path('', RedirectView.as_view(url='task/')),
    path('task/', TaskListView.as_view()),
    path('task/create/', TaskCreateOrUpdateView.as_view()),
    path('task/<task_id>/', TaskDetailView.as_view()),
    path('task/<task_id>/update/', TaskCreateOrUpdateView.as_view()),
    path('task/<pk>/delete/', TaskDeleteView.as_view()),

    path('user/create/', UserRegistrationView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view())
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)