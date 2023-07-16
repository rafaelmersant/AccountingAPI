# Django REST framework
from rest_framework import serializers

# Models
from .models import Person, Concept, Church, User

import hashlib


class UserSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'name', 'user_hash',
                  'user_role', 'created_date', 'created_by')

    def save(self, **kwargs):
        password = self.validated_data['password']
        if (len(password) < 32):
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
            self.validated_data["password"] = password
            
        return super().save(**kwargs)
    

class ShepherdSerializer(serializers.ModelSerializer):
    # church_id = serializers.IntegerField()

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification')


class ChurchReducedSerializer(serializers.ModelSerializer):
    shepherd = ShepherdSerializer()
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd', 'zone',
                  'created_date', 'created_by')


class ChurchAddUpdateSerializer(serializers.ModelSerializer):
    shepherd_id = serializers.IntegerField(required=False)
    local_title = serializers.CharField(max_length=255, required=False)
    location = serializers.CharField(max_length=255, required=False)
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd_id', 'zone',
                  'created_date', 'created_by')


class ChurchSerializer(serializers.ModelSerializer):
    shepherd = ShepherdSerializer(many=False, read_only=True)
        
    class Meta:
        model = Church
        fields = ('id', 'global_title', 'local_title', 'location', 'shepherd', 'zone',
                  'created_date', 'created_by', 'shepherd_full_name')


class PersonAddUpdateSerializer(serializers.ModelSerializer):
    identification = serializers.CharField(max_length=20, required=False)
    age = serializers.IntegerField(required=False)
    date_of_birth = serializers.DateField(required=False)
    
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification',
                  'age', 'gender', 'date_of_birth', 'ocupation', 'phone', 'cellphone',
                  'civil_status', 'address', 'reason_consultation', 'disease', 'doctor',
                  'created_date', 'created_by', 'reference')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification',
                  'age', 'gender', 'date_of_birth', 'ocupation', 'phone', 'cellphone',
                  'civil_status', 'address', 'reason_consultation', 'disease', 'doctor',
                  'created_date', 'created_by', 'full_name', 'reference')


class ConceptSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Concept
        fields = ('id', 'description', 'type', 'created_date', 'created_by')


