from django.db import models
from user import models as user_models
from exam import models as exam_models
# 报考系统应该不需要表，只需要展示出对应的考试和学生人数信息即可
class ExamReg(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(user_models.Student, on_delete=models.SET_NULL,null=True)
    exam_id = models.ForeignKey(exam_models.Exam, on_delete=models.SET_NULL,null=True)
    is_commit = models.BooleanField(default=False)