from datetime import datetime

from django.db import models
from django.db.models.deletion import DO_NOTHING
from party.models import Party
from settings.models import Student
from tinymce import models as tinymce_models

class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Election(models.Model):
    position = models.ManyToManyField(Position)
    vote_period_from = models.DateTimeField()
    vote_period_to= models.DateTimeField()
    created_at = models.DateField(auto_now_add=True,verbose_name='Election Year')

    def __str__(self):
        return str(self.created_at.year)

class Candidate(models.Model):
    student = models.ForeignKey(
            Student,
            on_delete=models.DO_NOTHING
        )
    profile = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/')
    election = models.ForeignKey(
            Election,
            on_delete=models.DO_NOTHING
        )
    position = models.ForeignKey(
            Position,
            on_delete=models.DO_NOTHING
        )
    party = models.ForeignKey(
            Party,
            on_delete=models.DO_NOTHING
        )
    
    def student_name(self):
        return self.student

class Vote(models.Model):
    vote_for = models.ForeignKey(
            Student,
            on_delete=models.DO_NOTHING,
            related_name='vote_for'
        )
    election = models.ForeignKey(
            Election,
            on_delete=models.DO_NOTHING
        )
    position = models.ForeignKey(
            Position,
            on_delete=models.DO_NOTHING
        )
    voter = models.ForeignKey(
            Student,
            on_delete=models.DO_NOTHING
        )
