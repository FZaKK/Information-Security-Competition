from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True) # 考号
    # self_number = models.IntegerField() # 身份证
    self_number = models.CharField(max_length=18,unique=True,null = False)
    name = models.CharField(max_length=30)
    school = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=12,unique=True,null=False)
    email = models.CharField(max_length=20)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

    def __str__(self):
        return self.name

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12,unique=True,null=False)
    password = models.CharField(max_length=30)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.name