# Django REST framework
from rest_framework import serializers

# Models
from .models import Person, Concept, Church, User, Attendance

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
    church_id = serializers.IntegerField(required=False)
    obrero_inicial = serializers.IntegerField(required=False)
    obrero_exhortador = serializers.IntegerField(required=False)
    obrero_licenciado = serializers.IntegerField(required=False)
    min_licenciado = serializers.IntegerField(required=False)
    min_ordenado = serializers.IntegerField(required=False)
    identification = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 'church_id',
                  'obrero_inicial', 'obrero_exhortador', 'obrero_licenciado', 'min_licenciado',
                  'min_ordenado', 'created_date', 'created_by')


class PersonSerializer(serializers.ModelSerializer):
    church = ChurchSerializer(many=False, read_only=True)
    church_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'identification', 'church', 'church_id',
                  'obrero_inicial', 'obrero_exhortador', 'obrero_licenciado', 'min_licenciado',
                  'min_ordenado', 'credential', 'credential_start', 'created_date', 'created_by',
                  'full_name')


class ConceptSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Concept
        fields = ('id', 'description', 'type', 'created_date', 'created_by')


class AttendanceAddUpdateSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(required=False)
        
    class Meta:
        model = Attendance
        fields = ('id', 'person_id', 'created_by', 'created_date', 'attendance_date')


class AttendanceSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
         
    class Meta:
        model = Attendance
        fields = ('id', 'person', 'created_by', 'created_date', 'attendance_date')

