from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib import messages

class UserRegistrationView(CreateView):
    model = User
    # django 自带的注册模板
    form_class = UserCreationForm
    # 注册成功后跳转的URL
    success_url = '/task/'

class UserLoginView(LoginView):
    template_name = 'auth/login_form.html'
    def form_invalid(self, form):
        messages.error(self.request, '登录失败！', extra_tags='danger')
        return super().form_invalid(form)


