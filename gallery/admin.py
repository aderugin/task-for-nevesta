# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Image
from .models import Tag
from .models import Tag2Image


class Tag2ImageInline(admin.TabularInline):
    model = Tag2Image


class ImageAdmin(admin.ModelAdmin):
    inlines = [Tag2ImageInline, ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Tag)
