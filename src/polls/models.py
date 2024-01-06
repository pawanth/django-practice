import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    '''
    Db table for questions.
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.question_text)
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        '''Check if question is recently published, i.e. within last 24 hours'''
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    '''
    Db table for choices.

    Multiple choices can be associated with one question.
    This is example of Many to one relationship ManyToOne from choices to question
    and One to many relationship from question to choices.
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)
