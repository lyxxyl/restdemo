# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20200116_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member_token',
            name='user',
        ),
        migrations.DeleteModel(
            name='member',
        ),
        migrations.DeleteModel(
            name='member_token',
        ),
    ]
