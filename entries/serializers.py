# Django REST framework
from rest_framework import serializers

from administration.serializers import ChurchReducedSerializer,  \
    ConceptSerializer, PersonSerializer

# Models
from .models import Entry, Item
from administration.models import Concept


class EntrySerializer(serializers.ModelSerializer):
    church = ChurchReducedSerializer(many=False, read_only=True)
    person = PersonSerializer(many=False, read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'person', 'note', 'period_year', 'period_month', 'church',
                  'created_date', 'created_by')


class EntryAddUpdateSerializer(serializers.ModelSerializer):
    church_id = serializers.IntegerField(required=False)
    person_id = serializers.IntegerField(required=False)

    class Meta:
        model = Entry
        fields = ('id', 'church_id', 'person_id', 'note', 'period_year', 'period_month',
                  'created_date', 'created_by')
        # optional_fields = ('church_id', 'person_id')


class ItemSerializer(serializers.ModelSerializer):
    entry = EntrySerializer(many=False)
    concept = ConceptSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'entry', 'concept', 'amount', 'reference', 'type')

    def save(self, **kwargs):
        try:
            concept_id = self.validated_data['concept_id']
            concept = Concept.objects.get(id=concept_id)
            concept.ocurrences += 1 
            concept.save()
        except Concept.DoesNotExist:
            pass
        
        return super().save(**kwargs)