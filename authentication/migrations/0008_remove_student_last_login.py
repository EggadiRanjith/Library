# Generated by Django 4.2.4 on 2023-09-04 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_student_roll_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='last_login',
        ),
    ]
