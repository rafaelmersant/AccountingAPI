# Django REST framework
from rest_framework import serializers

# Models
from .models import Person, Concept, Church, User


class UserSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'name', 'user_hash',
                  'user_role', 'created_date', 'created_by')


class ShepherdSerializer(serializers.ModelSerializer):
    # church_id = serializers.IntegerField()

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 
                  'created_date', 'created_by')


class ChurchReducedSerializer(serializers.ModelSerializer):
    shepherd_id = serializers.IntegerField()
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd_id',
                  'created_date', 'created_by')


class ChurchAddUpdateSerializer(serializers.ModelSerializer):
    shepherd_id = serializers.IntegerField(required=False)
    local_title = serializers.CharField(max_length=255, required=False)
    location = serializers.CharField(max_length=255, required=False)
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd_id',
                  'created_date', 'created_by')


class ChurchSerializer(serializers.ModelSerializer):
    shepherd = ShepherdSerializer(many=False, read_only=True)
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd',
                  'created_date', 'created_by')


class PersonAddUpdateSerializer(serializers.ModelSerializer):
    church_id = serializers.IntegerField(required=False)
    identification = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 'church_id',
                  'created_date', 'created_by')


class PersonSerializer(serializers.ModelSerializer):
    church = ChurchSerializer(many=False, read_only=True)
    church_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 'church', 'church_id',
                  'created_date', 'created_by')


class PersonSerializer(serializers.ModelSerializer):
    church = ChurchSerializer(many=False, read_only=True)
    church_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 'church', 'church_id',
                  'created_date', 'created_by')


class ConceptSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Concept
        fields = ('id', 'description', 'type', 'created_date', 'created_by')


