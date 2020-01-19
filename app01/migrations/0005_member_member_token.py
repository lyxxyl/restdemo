# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20200116_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='member_token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('token', models.CharField(max_length=64)),
                ('user', models.OneToOneField(to='app01.member')),
            ],
        ),
    ]
