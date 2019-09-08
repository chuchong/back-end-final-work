from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, ListView, DeleteView
from task.models import Task
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from back_end import settings
from .converter import handle

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
'''
def convert_image(self, task):
    # todo: change -> self.converted_image = ###
    task.converted_path = handle(self.image.path)
    print(task.converted_path)
    task.converted_image = "12.jpg"
'''


# 任务列表
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    queryset = None
    login_url = settings.LOGIN_URL
    paginate_by = 5

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Task.objects.filter(user=self.request.user)
        return self.queryset


# 任务详细信息
# LoginRequiredMixin 需要登录时，跳转到login_url的模块

class TaskDetailView(TemplateView):
    # templates文件夹的默认寻找template_name文件名为模板
    # template_name = 'task_list.html'
    template_name = 'task/task_detail.html'
    queryset = Task.objects.all()
    pk_url_kwargs = 'task_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset # queryset 初始化
        pk = self.kwargs.get(self.pk_url_kwargs) # id
        task = queryset.filter(pk=pk).first() # 搜出pk的结果，返回第一个
        if pk and not task:
            raise Http404('invalid pk')
        return task

    def get(self, request, *args, **kwargs):
        task = self.get_object()

        ctx = {
            'task': task
        }
        return self.render_to_response(ctx)


# 删除任务
class TaskDeleteView(DeleteView):
    model = Task
    success_message = '删除成功'
    success_url = '/task/'
    template_name_suffix = '_delete'

    def delete(self,*args,**kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(*args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')  # 无视 CSRF 验证
# 添加任务 或 更新任务
class TaskCreateOrUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'task/task_update.html'
    queryset = Task.objects.all()
    pk_url_kwargs = 'task_id'
    login_url = settings.LOGIN_URL
    success_message = '任务保存成功'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset  # queryset 初始化
        pk = self.kwargs.get(self.pk_url_kwargs)  # id
        task = queryset.filter(pk=pk).first()  # 搜出pk的结果，返回第一个
        if pk and not task:
            raise Http404('invalid pk')
        return task

    def get(self, request, *args, **kwargs):
        task = self.get_object()

        ctx = {
            'task': task
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        post_data = {key: request.POST.get(key) for key in ('title',)}
        post_data['image'] = request.FILES['image'] or None
        # 没有找到键值
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{}值为空!'.format(key), extra_tags='danger')
        # 若无 message 生成才执行
        if len(messages.get_messages(request)) == 0:
            # action 是 create
            if action == 'create':
                post_data['user'] = request.user
                task = Task.objects.create(**post_data)
                task.convert_image()
                messages.success(self.request, self.success_message)
            elif action == 'update':
                task = self.get_object()
                for key, value in post_data.items():
                    setattr(task, key, value)
                task.convert_image()
                task.save()
                messages.success(self.request, self.success_message)
            else:
                messages.error(self.request, '错误的请求！', extra_tags='danger')
            # 若保存成功， 返回任务列表
            return HttpResponseRedirect('/task/')
        ctx = {
            'task': self.get_object() if action == 'update' else None
        }
        return self.render_to_response(ctx)


