# Generated by Django 3.1.2 on 2020-10-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_questions_puplished_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='puplished_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
