# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Count
from .models import Tag, Tag2Image


class GalleryFilterForm(forms.Form):
    """
    Форма фильтрации картинок
    """
    def __init__(self, *args, **kwargs):
        super(GalleryFilterForm, self).__init__(*args, **kwargs)
        self.fields['exclude_tag'] = forms.MultipleChoiceField(
            choices=self.get_choices(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label=u'Исключить теги'
        )
        self.fields['include_tag'] = forms.MultipleChoiceField(
            choices=self.get_choices(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label=u'Включить теги'
        )

    def get_choices(self):
        return [(t.pk, t.name) for t in Tag.objects.all()]

    def get_queryset(self, qs):
        """
        Тут все сложно, много эксперементов было.
        Основная проблема с которой столкнулся - Django orm
        работает очень медленно с exclude / ~Q.
        Пришлошсь выдумывать множествами и исключениями.
        """
        if self.is_valid():
            exclude_tags = self.cleaned_data.get('exclude_tag') or []
            include_tags = self.cleaned_data.get('include_tag') or []
            indexes = None

            if include_tags:
                fq = Tag2Image.objects.filter(tag_id__in=include_tags)
                fq = fq.values('image_id').annotate(tag_count=Count('image_id')).filter(tag_count=len(include_tags))
                indexes = set(fq.values_list('image_id', flat=True))

            if exclude_tags:
                fq = Tag2Image.objects.filter(tag_id__in=exclude_tags)
                exclude_indexes = set(fq.values_list('image_id', flat=True))
                if not indexes:
                    # Если нет включающих тегов
                    return qs.exclude(id__in=exclude_indexes)
                else:
                    indexes = indexes.difference(exclude_indexes)

            if indexes:
                return qs.filter(id__in=indexes)
            elif include_tags or exclude_tags:
                # Если что-то выбрано в форме, но ничего не найдено,
                # выдаем пустой queryset
                return qs.none()

        return qs
