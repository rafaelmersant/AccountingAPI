# Django
from django_filters.rest_framework import DjangoFilterBackend

# Django REST framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Serializers
from . import serializers

# Others
import json

# Models
from .models import Entry, Item


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'note', 'church', 'person']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.EntryAddUpdateSerializer
        return serializers.EntrySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'reference', 'concept', 'type']
