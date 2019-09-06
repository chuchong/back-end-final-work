from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from task.models import Task
from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# 任务列表
class TaskListView(TemplateView):
    # templates文件夹的默认寻找template_name文件名为模板
    template_name = 'task_list.html'
    # 请求内容
    def get(self, request, *args, **kwargs):
        # 所有任务
        queryset = Task.objects.all()
        ctx = {
            'tasks': queryset
        }
        # from generic views
        # 把模板转换成html, ctx要词典变量
        return self.render_to_response(ctx)

# 任务详细信息
class TaskDetailView(TemplateView):
    template_name = 'task_detail.html'
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


# @method_decorator(csrf_exempt, name='dispatch')  # 无视 CSRF 验证
# 添加任务 或 更新任务
class TaskCreateOrUpdateView(TemplateView):
    template_name = 'task_update.html'
    queryset = Task.objects.all()
    pk_url_kwargs = 'task_id'
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
        post_data = {key: request.POST.get(key) for key in ('title', 'user')}
        # 没有找到键值
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{}值为空!'.format(key), extra_tags='danger')
        # 若无 message 生成才执行
        if len(messages.get_messages(request)) == 0:
            # action 是 create
            if action == 'create':
                task = Task.objects.create(**post_data)
                messages.success(self.request, self.success_message)
            elif action == 'update':
                task = self.get_object()
                for key, value in post_data.items():
                    setattr(task, key, value)
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
