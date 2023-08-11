from django.contrib import admin

# Register your models here.
# app01/admin.py:
from exam.models import Exam,ExamOrder,Paper,Question
from user.models import Student,Teacher
from marking.models import AnswerRecord,ExamScore
 
# 注册Model类. 下面注册了这就不用注册了
# admin.site.register(Student)
# admin.site.register(Teacher)
# admin.site.register(Question)
# admin.site.register(Paper)
# admin.site.register(Exam)
# admin.site.register(ExamOrder)
# admin.site.register(AnswerRecord)
# admin.site.register(ExamScore)

class StuAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'self_number','name', 'school', 'password', 'phone', 'email')
    list_filter = ('self_number','name', 'school','phone')
    # list_editable = ('name', 'school', 'password', 'phone', 'email')

class TeacherAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'name', 'phone', 'password')
    list_filter = ('name', 'phone')

class QuestionAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'type', 'question', 'answer')
    list_filter = ('type','question')

class PaperAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'question_ids', 'type')
    list_filter = ('type',)

class ExamAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'name', 'date', 'start_time', 'end_time', 'place', 'is_online', 'is_beginning', 'max_students')
    list_filter = ('name', 'date', 'place', 'is_online', 'is_beginning', 'max_students')

class ExamOrderAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'exam', 'student', 'paid', 'payment','pay_time')
    list_filter = ('exam', 'student', 'paid', 'payment','pay_time')

class AnswerRecordAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'exam', 'student_id', 'question_id','score','is_marked')
    list_filter = ('exam', 'student_id', 'question_id','is_marked')

class ExamScoreAdmin(admin.ModelAdmin):
    list_per_page = 10  # 默认为100条
    actions_on_top = True # top actions button
    list_display = ('id', 'exam_id', 'student_id', 'teacher_id','score')
    list_filter = ('exam_id', 'student_id', 'teacher_id','score')

admin.site.register(Student,StuAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Paper,PaperAdmin)
admin.site.register(Exam,ExamAdmin)
admin.site.register(ExamOrder,ExamOrderAdmin)
admin.site.register(AnswerRecord,AnswerRecordAdmin)
admin.site.register(ExamScore,ExamScoreAdmin)

admin.site.site_header = 'CET管理后台'  # 设置header
admin.site.site_title = 'CET管理后台'   # 设置title
admin.site.index_title = 'CET管理后台'

