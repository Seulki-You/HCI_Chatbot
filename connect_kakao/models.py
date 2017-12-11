# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Lecture(models.Model):
    lectureid = models.IntegerField(db_column='lectureID', primary_key=True)  # Field name made lowercase.
    professor = models.CharField(max_length=100, blank=True, null=True)
    lecturename = models.CharField(db_column='lectureName', max_length=200)  # Field name made lowercase.
    exam = models.CharField(max_length=10, blank=True, null=True)
    attendance = models.CharField(max_length=10, blank=True, null=True)
    team = models.CharField(max_length=10, blank=True, null=True)
    homework = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lecture'
