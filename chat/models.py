from django.db import models
from django.utils import timezone

# Create your models here.
class GroupMessage(models.Model):
    """记录群组消息
     1 主要为测试用户登录
     2 以及异步的数据库操作
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    groupname = models.CharField(max_length=60)
    message = models.CharField(max_length=120)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s 群组：%s, 用户 %s, 时间 %s.'% (self.message,self.groupname, self.user.username, self.create_time)
