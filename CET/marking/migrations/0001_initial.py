# Generated by Django 4.1 on 2023-08-01 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
                ('exam_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.exam')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.student')),
                ('teacher_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher')),
            ],
            options={
                'verbose_name': '考试成绩',
                'verbose_name_plural': '考试成绩',
            },
        ),
        migrations.CreateModel(
            name='AnswerRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(null=True)),
                ('stu_answer', models.TextField(null=True)),
                ('is_marked', models.BooleanField(null=True)),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.exam')),
                ('question_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.question')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.student')),
            ],
            options={
                'verbose_name': '答题情况',
                'verbose_name_plural': '答题情况',
            },
        ),
    ]
