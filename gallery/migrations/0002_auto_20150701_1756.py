# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag2Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag2gallery',
            name='image',
        ),
        migrations.RemoveField(
            model_name='tag2gallery',
            name='tag',
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u0422\u0435\u0433', 'verbose_name_plural': '\u0422\u0435\u0433\u0438'},
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(max_length=255, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='like',
            name='image',
            field=models.ForeignKey(related_name='likes', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', to='gallery.Image'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Tag2Gallery',
        ),
        migrations.AddField(
            model_name='tag2image',
            name='image',
            field=models.ForeignKey(related_name='tags', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', to='gallery.Image'),
        ),
        migrations.AddField(
            model_name='tag2image',
            name='tag',
            field=models.ForeignKey(related_name='tags', verbose_name='\u0422\u0435\u0433', to='gallery.Tag'),
        ),
    ]
