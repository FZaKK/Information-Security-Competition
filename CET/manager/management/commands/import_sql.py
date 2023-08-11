from django.core.management.base import BaseCommand
from django.db import connection
from manager import db_operation as db
from datetime import datetime ,time
import os
import csv


class Command(BaseCommand):
    help = 'Import Test SQL file'
    

    def handle(self, *args, **options):
        def import_questions():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            question_file = os.path.join(current_dir, '../../../../samples/que-test-sample.csv')
            with open(question_file,'r',newline='',encoding='utf-8') as file:
                reader=csv.reader(file)
                for row in reader:
                    question_type=int(row[0])
                    question_text=row[1]
                    question_anwser=row[2]
                    db.exam.insert_question(question_type,question_text,question_anwser)
        
        print("\033[1;32mStarting Importing Test SQL file\033[0m")

        stu1,err = db.user.insert_stu('110000200201010000', '学生1', 'NKU', '123456',
                           '13888888880', '1@mail.nankai.edu.cn')
        stu2,err = db.user.insert_stu('110000200201010001', '学生2', 'NKU', '123456',
                           '13888888881', '2@mail.nankai.edu.cn')
        stu3,err = db.user.insert_stu('110000200201010002', '学生3', 'NKU', '123456',
                           '13888888882', '3@mail.nankai.edu.cn')
        stu4,err = db.user.insert_stu('110000200201010003', '学生4', 'NKU', '123456',
                           '13888888883', '4@mail.nankai.edu.cn')
        stu5,err = db.user.insert_stu('110000200201010004', '学生5', 'NKU', '123456',
                           '13888888884', '5@mail.nankai.edu.cn')

        tea1,err = db.user.insert_tea('老师1', '13888888800', '123456')
        tea2,err = db.user.insert_tea('老师2', '13888888801', '123456')
        print("\033[1;32mFinished Importing Users\033[0m")
        import_questions()
        que_id = db.exam_m.Question.objects.latest('id').id
        if que_id:
            db.exam.insert_paper(','.join([str(que_id-7), str(que_id-6), str(que_id-5), str(que_id-4)]), 0)
            db.exam.insert_paper(','.join([str(que_id-3), str(que_id-2), str(que_id-1), str(que_id)]), 1)
        else:
            print("\033[1;31mError Importing Papers\033[0m")

        date_string = "2077-01-01 12:00:00"
        date_format = "%Y-%m-%d %H:%M:%S"
        date_1 = datetime.strptime(date_string, date_format)
        papers, err = db.exam.select_all_paper()
        pid1 = 0
        pid2 = 0
        if papers and papers.count()>1 and err:
            pid1 = papers[papers.count()-1].id
            pid2 = papers[papers.count()-2].id
            start_time = time(17, 0, 0)
            end_time = time(18, 0, 0)
            db.exam.insert_exam('eTJU',date_1,start_time,end_time,True,True, 'TJU', pid1, 10)
            db.exam.insert_exam('eNKU',datetime.now(),start_time,end_time,True,True, 'NKU', pid2, 10)
        else :
            print("\033[1;31mError Importing Exam\033[0m")
        
        exams, err = db.exam.select_all_exam()
        eid1 = 0
        eid2 = 0
        stu1_id = stu1.id if stu1 else 0
        stu2_id = stu2.id if stu2 else 0
        if exams and exams.count()>1 and err and stu1_id and stu2_id:
            eid1 = exams[exams.count()-1].id
            eid2 = exams[exams.count()-2].id
            db.exam.insert_ExamOder(eid1, stu1_id, True, 25.0)
            db.exam.insert_ExamOder(eid2, stu2_id, False, 0.0)
            # added reg, stu1 and stu2 registed exam1 and exam2
            db.exam2.insert_exam_arrangement(stu1_id,eid1)
            db.exam2.insert_exam_arrangement(stu2_id,eid2)
        else:
            print("\033[1;32mError Importing Exam oder\033[0m")

        print("\033[1;32mFinished Importing Exam\033[0m")

        # stu 2 joined exam 2
        ques , err = db.exam.select_all_que()
        if ques and ques.count()>1 and err:
            db.marking.insert_AnswerRecord(eid2,stu2_id,ques[ques.count()-1].id,True)
            db.marking.insert_AnswerRecord(eid2,stu2_id,ques[ques.count()-2].id,False)
            db.marking.insert_AnswerRecord(eid2,stu2_id,ques[ques.count()-3].id,False)
            db.marking.insert_AnswerRecord(eid2,stu2_id,ques[ques.count()-4].id,False)
            db.marking.insert_ExamScore(eid2,stu2_id,tea1.id if tea1 else 0,25)
        else :
            print("\033[1;32mError Importing Question\033[0m")
        print("\033[1;32mFinished Importing Marking\033[0m")

        print("\033[1;32mFinished Importing Test SQL file\033[0m")

