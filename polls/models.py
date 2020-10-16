from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    puplished_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_puplished_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.puplished_date <= now
    was_puplished_recently.admin_order_field = 'puplished_date'
    was_puplished_recently.boolean = True
    was_puplished_recently.short_description = ' puplished recently ?'


class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    vote_tally = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
