from django.db import models
from exam import models as exam_models
from user import models as user_models
# from 

# 答题情况表
class AnswerRecord(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(exam_models.Exam, on_delete=models.SET_NULL,null=True)
    student_id = models.ForeignKey(user_models.Student, on_delete=models.SET_NULL,null=True)
    question_id = models.ForeignKey(exam_models.Question, on_delete=models.SET_NULL,null=True)
    # is_right = models.BooleanField()
    score = models.IntegerField(null=True) # 对的就有分， 错的0分
    stu_answer = models.TextField(null=True)
    is_marked = models.BooleanField(null=True)

    class Meta:
        verbose_name = '答题情况'
        verbose_name_plural = '答题情况'

    # cannot return an int
    # def __str__(self): 
    #     return self.id

# 考试成绩表
class ExamScore(models.Model):
    id = models.AutoField(primary_key=True)
    exam_id = models.ForeignKey(exam_models.Exam, on_delete=models.SET_NULL,null=True)
    student_id = models.ForeignKey(user_models.Student, on_delete=models.SET_NULL,null=True)
    teacher_id = models.ForeignKey(user_models.Teacher, on_delete=models.SET_NULL,null=True)
    score = models.IntegerField()

    class Meta:
        verbose_name = '考试成绩'
        verbose_name_plural = '考试成绩'
    
    # def __str__(self):
    #     return self.id