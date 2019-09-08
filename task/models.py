from django.db import models
from django.contrib.auth.models import User
from back_end import settings
from .converter import handle
import os
# Create your models here.
os.path.join(settings.MEDIA_DIR, 'images/')

class Task(models.Model):
    title = models.CharField('标题', max_length=128, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True,
        width_field='width_field', height_field='height_field')
    converted_image1 = models.ImageField(
        null=True, blank=True,
        width_field='width_field', height_field='height_field'
    )
    converted_image2 = models.ImageField(
        null=True, blank=True,
        width_field='width_field', height_field='height_field'
    )

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    created_at = models.DateTimeField('生成时间', auto_now_add=True)

    def __init__(self, *args, **kargs):
        super(Task, self).__init__(*args, **kargs)
        self.convert_image()



    # 调用图片处理算法
    def convert_image(self):
        # todo: change -> self.converted_image = ###
        if self.image:
            handle(self.image.path)
            self.converted_image1 = self.image.name + '__1.jpg'
            self.converted_image2 = self.image.name + '__2.jpg'



    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        if os.path.exists(self.converted_image1.path and self.converted_image2.path):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.converted_image1.path))
            os.remove(os.path.join(settings.MEDIA_ROOT, self.converted_image2.path))
        super(Task, self).delete(*args, **kargs)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
