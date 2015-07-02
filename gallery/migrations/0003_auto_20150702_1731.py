# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150701_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag2image',
            options={'verbose_name': '\u0422\u0435\u0433 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f', 'verbose_name_plural': '\u0422\u0435\u0433\u0438 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f'},
        ),
        migrations.AddField(
            model_name='image',
            name='like_count',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
    ]
