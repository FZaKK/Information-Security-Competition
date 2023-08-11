from django.core.management.base import BaseCommand
from user.models import Student,Teacher
from exam.models import Exam,ExamOrder,Paper,Question
from marking.models import AnswerRecord,ExamScore
class Command(BaseCommand):
    help = 'clear SQL db'

    def handle(self, *args, **options):
        print("\033[1;32mStarting clear SQL db\033[0m")
        try:
            ExamScore.objects.all().delete()
            AnswerRecord.objects.all().delete()
            ExamOrder.objects.all().delete()
            Exam.objects.all().delete()
            Paper.objects.all().delete()
            Question.objects.all().delete()
            Student.objects.all().delete()
            Teacher.objects.all().delete()
        except Exception as e:
            print("\033[1;31mFailed to clear SQL db:\033[0m\n%s",e)
        print("\033[1;32mFinished clear SQL db\033[0m")