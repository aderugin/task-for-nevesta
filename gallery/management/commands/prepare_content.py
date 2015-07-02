# -*- coding: utf-8 -*-
import csv
from random import randint

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from ...models import Image
from ...models import Tag
from ...models import Tag2Image
from ...models import Like


USER_FILE = settings.MEDIA_ROOT + 'users.csv'

TAG_FILE = settings.MEDIA_ROOT + 'tags.txt'

GALLERY_FILE = settings.MEDIA_ROOT + 'photos.csv'


class Command(BaseCommand):
    # args = 'json, xml --mctrade'
    help = u'Заполнение базы данными'

    def get_random_user(self):
        count = User.objects.count()
        return User.objects.all()[randint(0, count - 1)]

    def get_random_tag(self):
        count = Tag.objects.count()
        return Tag.objects.all()[randint(0, count - 1)]

    def handle(self, *args, **options):
        # Создание пользователей
        with open(USER_FILE, 'r') as csvfile:
            User.objects.exclude(username='admin').delete()

            reader = list(csv.reader(csvfile, delimiter=';'))
            for line in reader[1:]:
                try:
                    user = User.objects.create(
                        first_name=line[1].split(' ')[0],
                        last_name=line[1].split(' ')[1],
                        username=line[0]
                    )
                    self.stdout.write(u'[%s] Создан пользователь' % user.username)
                except Exception:
                    pass

        # Создание тегов
        with open(TAG_FILE, 'r') as f:
            Tag.objects.all().delete()

            raw_tags = f.read().split(' ')
            for tag in raw_tags:
                Tag.objects.create(name=tag)
                self.stdout.write(u'Добавлен тег')

        # Создание изображений
        with open(GALLERY_FILE, 'r') as csvfile:
            Image.objects.all().delete()

            reader = list(csv.reader(csvfile, delimiter=';'))
            for line in reader[1:]:
                image = Image.objects.create(
                    url=line[1],
                    user=self.get_random_user(),
                    timestamp=line[2],
                )

                # Создание лайка
                for x in range(randint(7, 15)):
                    Like.objects.create(
                        image=image,
                        user=self.get_random_user()
                    )

                # Создание связи тег-изображение
                for i in range(randint(1, 8)):
                    Tag2Image.objects.create(
                        image=image,
                        tag=self.get_random_tag()
                    )
                self.stdout.write(u'Добавлено изображение')
