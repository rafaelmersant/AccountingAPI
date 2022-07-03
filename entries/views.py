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
            self.queryset = self.queryset.filter(period_month=period_month, period_year=period_year)
        
        if start_date is not None and end_date is not None:
            self.queryset = self.queryset.filter(created_date__date__gte=start_date, created_date__date__lte=end_date)
        
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
        
