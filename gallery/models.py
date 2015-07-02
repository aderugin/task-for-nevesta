# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


# -----------------------------------------------------------------------------
class Image(models.Model):

    class Meta:
        verbose_name = u'Изображение галереи'
        verbose_name_plural = u'Изображения галереи'
        ordering = ['-timestamp', 'like_count', ]

    url = models.URLField(verbose_name=u'URL', max_length=255)
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    timestamp = models.DateTimeField(verbose_name=u'Дата создания')
    # Денормалиованные лайки
    like_count = models.PositiveIntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.url


# -----------------------------------------------------------------------------
class Like(models.Model):
    image = models.ForeignKey(Image, verbose_name=u'Изображение', related_name='likes')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')


# -----------------------------------------------------------------------------
class Tag(models.Model):

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'

    name = models.CharField(verbose_name=u'Тег', max_length=255)

    def __unicode__(self):
        return self.name


# -----------------------------------------------------------------------------
class Tag2Image(models.Model):

    class Meta:
        verbose_name = u'Тег изображения'
        verbose_name_plural = u'Теги изображения'

    tag = models.ForeignKey(Tag, verbose_name=u'Тег', related_name='tags')
    image = models.ForeignKey(Image, verbose_name=u'Изображение', related_name='tags')

    def __unicode__(self):
        return self.tag.name


# -----------------------------------------------------------------------------
@receiver([post_save, post_delete], sender=Like)
def like_save(sender, instance, **kwargs):
    """
    Денормализация лайков
    """
    image = instance.image
    if image:
        image.like_count = image.likes.count()
        image.save()
