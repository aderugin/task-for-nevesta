# -*- coding: utf-8 -*-
import string

from django.views.generic import ListView
from django.db.models import Prefetch

from .models import Image
from .models import Tag2Image
from .forms import GalleryFilterForm


class GalleryListView(ListView):
    model = Image
    paginate_by = 20
    template_name = 'gallery/image_list.html'

    def get_filter(self):
        """
        Фильтр
        """
        if not hasattr(self, '_product_filter'):
            self._product_filter = GalleryFilterForm(self.request.GET)
        return getattr(self, '_product_filter', None)

    def get_sorted_queryset(self, qs):
        """
        Сортировка по дате и по количеству лайков
        """
        sortable = ['like_count', 'timestamp', ]
        ordering = self.request.GET.get('order_by', '')
        asc = not ordering.startswith('-')
        ordering = ordering.replace('-', '')
        if ordering and ordering in sortable:
            qs = qs.order_by('{0}{1}'.format('-' if not asc else '', ordering))
        return qs

    def get_queryset(self):
        qs = super(GalleryListView, self).get_queryset()
        qs = self.get_filter().get_queryset(qs)
        qs = self.get_sorted_queryset(qs)
        return qs

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, has_other_pages = super(GalleryListView, self).paginate_queryset(queryset, page_size)

        # Джоиним теги
        tags_prefetch = Prefetch(
            'tags',
            queryset=Tag2Image.objects.select_related('tag').all()
        )

        qs = object_list.prefetch_related('likes', tags_prefetch)
        return paginator, page, qs, has_other_pages

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['filter'] = self.get_filter()
        return context
