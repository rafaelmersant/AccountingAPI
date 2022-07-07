# Django REST framework
from rest_framework import serializers

from administration.serializers import ChurchReducedSerializer,  \
    ConceptSerializer, PersonSerializer, UserSerializer

# Models
from .models import Entry, Item
from administration.models import Concept


class EntryItemReducedSerializer(serializers.ModelSerializer):
    concept = ConceptSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'concept', 'amount', 'reference', 'type',  \
                  'method', 'period_year', 'period_month')


class EntrySerializer(serializers.ModelSerializer):
    church = ChurchReducedSerializer(many=False, read_only=True)
    person = PersonSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
    item_set = EntryItemReducedSerializer(many=True)

    class Meta:
        model = Entry
        fields = ('id', 'person', 'note', 'period_year', 'period_month', 'church',
                  'created_date', 'created_by', 'total_amount', 'item_set')
        
    
class EntryAddUpdateSerializer(serializers.ModelSerializer):
    church_id = serializers.IntegerField(required=False)
    person_id = serializers.IntegerField(required=False)

    class Meta:
        model = Entry
        fields = ('id', 'church_id', 'person_id', 'note', 'period_year', 'period_month',
                  'total_amount', 'created_date', 'created_by')
        # optional_fields = ('church_id', 'person_id')


class EntryItemSerializer(serializers.ModelSerializer):
    entry = EntrySerializer(many=False)
    concept = ConceptSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'entry', 'concept', 'amount', 'reference', 'type', \
                  'method', 'period_year', 'period_month')


class EntryItemAddUpdateSerializer(serializers.ModelSerializer):
    concept_id = serializers.IntegerField()

    class Meta:
        model = Item
        fields = ('id', 'entry_id', 'concept_id', 'amount', 'reference', 'type', \
                  'method', 'period_year', 'period_month')

    def create(self, validated_data):
        entry_id = self.context['entry_id']
        return Item.objects.create(entry_id=entry_id, **validated_data)

    def save(self, **kwargs):
        try:
            concept_id = self.validated_data['concept_id']
            concept = Concept.objects.get(id=concept_id)
            concept.ocurrences += 1 
            concept.save()
        except Concept.DoesNotExist:
            pass

        # try:
        #     amount = self.validated_data['amount']

        #     entry_id = self.context['entry_id']
        #     entry = Entry.objects.get(id=entry_id)
        #     try:
        #         if self.context['item_id'] is not None:
        #             item_id = self.context['item_id'] 
        #             item = Item.objects.get(id=item_id)
        #             entry.total_amount -= item.amount
        #             entry.total_amount += amount
        #     except Item.DoesNotExist:
        #         pass
        #         # entry.total_amount += amount

        #     entry.save()
        # except Entry.DoesNotExist:
        #     pass
        
        return super().save(**kwargs)


class ChurchReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    global_title = serializers.CharField(max_length=255)
    percent_concilio = serializers.DecimalField(max_digits=18, decimal_places=6, default=0)
    ofrenda_misionera = serializers.DecimalField(max_digits=18, decimal_places=6, default=0)
    period_month = serializers.IntegerField()
    period_year = serializers.IntegerField()
    