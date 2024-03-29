# Django
from django_filters.rest_framework import DjangoFilterBackend

# Django REST framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from accounting import paginations

# Serializers
from . import serializers

# Others
import json

# Models
from .models import Entry, Item

import datetime
from datetime import datetime as date_format


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.prefetch_related("item_set__concept") \
                            .prefetch_related("item_set") \
                            .prefetch_related("church") \
                            .prefetch_related("person") \
                            .prefetch_related("church__shepherd") \
                            .prefetch_related("person__church") \
                            .prefetch_related("person__church__shepherd") \
                            .prefetch_related('created_by').all()

    serializer_class = serializers.EntrySerializer
    pagination_class = paginations.EntryListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'note', 'church', 'church_id', 'person', 'person_id', 'total_amount']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.EntryAddUpdateSerializer
        return serializers.EntrySerializer
    
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        dashboard = self.request.query_params.get('dashboard', None)
        period_month = self.request.query_params.get('period_month', None)
        period_year = self.request.query_params.get('period_year', None)

        if dashboard is not None and period_month != '0':
            self.queryset = self.queryset.filter(item__period_month=period_month, item__period_year=period_year)
        
        if start_date is not None and end_date is not None:
            _start_date = date_format.strptime(start_date, '%Y-%m-%d')
            _end_date = date_format.strptime(end_date, '%Y-%m-%d')

            print(f'start date: {_start_date}')
            print(f'end date: {_end_date}')

            self.queryset = self.queryset.filter(created_date__date__gte=_start_date, \
                                                created_date__date__lte=_end_date)

        return self.queryset


class EntryItemViewSet(ModelViewSet):
    serializer_class = serializers.EntryItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'reference', 'concept', 'type']

    def get_queryset(self):
        return Item.objects \
            .prefetch_related("entry") \
            .select_related("concept") \
            .prefetch_related('entry__church') \
            .prefetch_related('entry__person') \
            .prefetch_related('entry__created_by') \
            .prefetch_related('entry__person__church') \
            .prefetch_related('entry__person__church__shepherd') \
            .prefetch_related('entry__item_set') \
            .prefetch_related('entry__item_set__concept') \
            .filter(entry_id=self.kwargs["entry_pk"])
       
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.EntryItemAddUpdateSerializer
        return serializers.EntryItemSerializer
    
    def get_serializer_context(self):
        item_id = 0

        if self.kwargs.__len__() > 1:
            item_id = self.kwargs['pk']
        
        return {'entry_id': self.kwargs['entry_pk'], 'item_id': item_id}
        

class ChurchReportViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = serializers.ChurchReportSerializer

    def get_queryset(self):
       period_month = self.request.query_params.get('period_month', None)
       period_year = self.request.query_params.get('period_year', None)
       church_id = self.request.query_params.get('church_id', None)

       if period_month is not None and period_year is not None:
           query = """
                    select 
                        c.id, c.global_title, strftime('%m', h.created_date) as period_month, 
                        strftime('%Y', h.created_date) as period_year, 
                        IFNULL((select d.amount from entries_item d 
                        where d.entry_id = h.id and d.concept_id = 1), 0) percent_concilio,
                        IFNULL((select d.amount from entries_item d 
                        where d.entry_id = h.id and d.concept_id = 2), 0) ofrenda_misionera
                    from administration_church c
                    left outer join entries_entry h on h.church_id = c.id 
                             and strftime('%m%Y', h.created_date) = '#periodMonth##periodYear#'
                             and h.id in (select d2.entry_id from entries_item d2 
                                          where d2.concept_id = 1 or d2.concept_id = 2)
                    #filterChurch#
                    order by 2
                    """.replace("#periodMonth#", period_month) \
                       .replace("#periodYear#", period_year) \
                       
           if church_id is not None:
              query = query.replace("#filterChurch#", f' where c.id = {church_id} ')
           else:
              query = query.replace("#filterChurch#", '')

           print(query)
           return Item.objects.raw(query)