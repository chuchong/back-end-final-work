from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField('标题', max_length=128, null=False)
    user = models.CharField('用户', max_length=64, null=False)
    created_at = models.DateTimeField('生成时间', auto_now_add=True)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)