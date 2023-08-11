from typing import List
from django.test import TestCase
from manager import db_operation
from datetime import datetime,time


# 为了节省时间，带有外键约束的测试都默认id=1，即单个测试生效，一起测试不行
# python .\manage.py test manager.tests.db_test
class db_test(TestCase):
    def test_user_stu(self):
        db_operation.user.insert_stu(
            '2', '张三', 'NKU', '123456', '18888888889', '123@qq.com')
        stu = db_operation.user_m.Student.objects.latest('id')
        db_operation.user.select_stu_by_id(stu.id)
        db_operation.user.select_stu_by_phone(stu.phone)
        db_operation.user.update_stu(
            stu.self_number, '李四', 'NKU', '123456', '18888888888', '123@qq.com',stu.id)
        db_operation.user.delete_stu(stu.id)

    def test_user_tea(self):
        db_operation.user.insert_tea('李四', '18888888888','123456')
        tea = db_operation.user_m.Teacher.objects.latest('id')
        db_operation.user.select_tea_by_id(tea.id)
        db_operation.user.select_tea_by_phone(tea.phone)
        db_operation.user.update_tea(tea.id, '李5','18888888888', '123456')
        db_operation.user.delete_tea(tea.id)

    def test_exam_alle(self):
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        exams, ok = db_operation.exam.select_all_exam()
        if ok and exams:
            print(exams[0].date)

    def test_exam_alle_bystu(self):
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.exam.insert_ExamOder(1, 1, True, 1.0)
        exams, ok = db_operation.exam.select_all_exam_by_stu(1)
        if ok and exams:
            for exam in exams:
                if exam:
                    print(exam.date)

    def test_exam_que(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        que = db_operation.exam_m.Question.objects.latest('id')
        db_operation.exam.select_question_by_id(que.id)
        db_operation.exam.update_question(que.id, 2, '题目2', '选项2')
        db_operation.exam.delete_question(que.id)

    def test_exam_Paper(self):
        db_operation.exam.insert_paper('1', 1)
        p = db_operation.exam_m.Paper.objects.latest('id')
        db_operation.exam.select_paper_by_id(p.id)
        db_operation.exam.update_paper(p.id, '2', 1)
        db_operation.exam.delete_paper(p.id)

    def test_exam_exam(self):
        db_operation.exam.insert_paper('1', 1)  # fk
        date_string = "2022-01-01 12:00:00"
        date_format = "%Y-%m-%d %H:%M:%S"
        date_object = datetime.strptime(date_string, date_format)
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',date_object,start_time,end_time,True,False, 'nku', 1, 1)
        exam = db_operation.exam_m.Exam.objects.latest('id')
        db_operation.exam.select_exam_by_id(exam.id)
        db_operation.exam.update_exam(exam.id,'e1', datetime.now(), start_time,end_time,True,False,'tju', 1, 1)
        db_operation.exam.delete_exam(exam.id)

    def test_exam_order(self):
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.exam.insert_ExamOder(1, 1, True, 1.0)

        db_operation.exam.select_ExamOder_by_id(1)

        db_operation.exam.delete_ExamOder(1)

    def test_marking_ans_rec(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')

        db_operation.marking.insert_AnswerRecord(1, 1, 1, 1,"ss",False)
        db_operation.marking.select_AnswerRecord_by_id(1)
        db_operation.marking.update_AnswerRecord(1, 1, 1, 1,1,True)
        db_operation.marking.delete_AnswerRecord(1)

    def test_marking_ExamScore(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.user.insert_tea('李四', '123456', '18888888888')

        db_operation.marking.insert_ExamScore(1, 1, 1, 99)

        db_operation.marking.select_ExamScore_by_id(1)
        db_operation.marking.update_ExamScore(1, 1, 1, 1, 100)
        db_operation.marking.delete_ExamScore(1)

    def test_marking_allEscore(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.user.insert_tea('李四', '123456', '18888888888')

        db_operation.marking.insert_ExamScore(1, 1, 1, 99)
        db_operation.marking.insert_ExamScore(1, 1, 1, 0)

        e , ok = db_operation.marking.select_all_EScore()
        if ok and e:
            for ee in e:
                print(ee.score)

    def test_marking_allEscore_bystu(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.user.insert_tea('李四', '123456', '18888888888')

        db_operation.marking.insert_ExamScore(1, 1, 1, 99)

        e, ok = db_operation.marking.select_all_EScore_by_stu(1)
        if ok and e:
            for ee in e:
                print(ee.score)

    def test_reg_exam_arrange(self):
        db_operation.exam.insert_question(1, '题目1', '选项1')
        db_operation.exam.insert_paper('1', 1)  # fk
        start_time = time(9, 0, 0)
        end_time = time(10, 0, 0)
        db_operation.exam.insert_exam('e1',datetime.now(),start_time,end_time,True,False, 'nku', 1, 1)
        db_operation.user.insert_stu(
            '1', '张三', 'NKU', '123456', '18888888888', '123@qq.com')
        db_operation.exam2.insert_exam_arrangement(1,1)
        db_operation.exam2.select_exam_arrangement_by_stuid(1)
        db_operation.exam2.delete_exam_arrangement_by_id(1)
