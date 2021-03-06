# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lectureid', models.IntegerField(db_column='lectureID', primary_key=True, serialize=False)),
                ('professor', models.CharField(blank=True, max_length=100, null=True)),
                ('lecturename', models.CharField(db_column='lectureName', max_length=200)),
                ('exam', models.CharField(blank=True, max_length=10, null=True)),
                ('attendance', models.CharField(blank=True, max_length=10, null=True)),
                ('team', models.CharField(blank=True, max_length=10, null=True)),
                ('homework', models.CharField(blank=True, max_length=10, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'lecture',
            },
        ),
    ]
