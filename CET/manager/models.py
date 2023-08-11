from django.db import models

# 管理员由django自己在`auth_user`表中管理，不需要额外建表

# 此处给一个测试用表，随便蹂躏
class TestTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    test = models.DateField(auto_now_add=True)
    is_commit = models.BooleanField(default=False)
