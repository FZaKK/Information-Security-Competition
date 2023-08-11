from django.db import models
from django.utils import timezone
from datetime import time
from user import models as user_models

# 题目
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField() # 0为选择题，1为填空题
    question = models.TextField(max_length=1024)
    answer = models.CharField(max_length=50)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'

    # def __str__(self):
    #     return self.id

# 试卷
class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    question_ids = models.CharField(max_length=512) 
    # 这里使用的是用符号分割开的问题号的列表，如果不方便可以以后优化。eg: [1,2,3]   
    type = models.IntegerField()

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'

    # def __str__(self):
    #     return self.id

# 考试安排
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    date = models.DateField()
    start_time = models.TimeField(default=time(0, 0, 0))
    end_time = models.TimeField(default=time(0, 0, 0))
    place = models.CharField(max_length=30)
    is_online=models.BooleanField()
    is_beginning=models.BooleanField()
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL,null=True)
    max_students = models.IntegerField()

    class Meta:
        verbose_name = '考试安排'
        verbose_name_plural = '考试安排'

    def __str__(self):
        return self.name

# 订单记录
class ExamOrder(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL,null=True)
    student = models.ForeignKey(user_models.Student, on_delete=models.SET_NULL,null=True)
    paid = models.BooleanField()
    payment = models.FloatField()
    pay_time = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = '订单记录'
        verbose_name_plural = '订单记录'

    # def __str__(self):
    #     return self.id

