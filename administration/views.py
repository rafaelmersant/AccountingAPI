# Django
from django_filters.rest_framework import DjangoFilterBackend

# Django REST framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Serializers
from . import serializers

# Paginations
from accounting import paginations

# Others
import json
import hashlib

# Models
from .models import User, Concept, Church, Person


class ConceptViewSet(ModelViewSet):
    queryset = Concept.objects.all()
    serializer_class = serializers.ConceptSerializer
    pagination_class = paginations.StandardResultsSetPaginationLevelHighest
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'description', 'type']
    search_fields = ['description',]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'username', 'email', 'name', 'user_role', 'user_hash', 'created_date']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UserSerializer
        return serializers.UserSerializer


class UserLogin(generics.ListCreateAPIView):
    """ User Login view.

    POST call that allow to login the users.
    """
    serializer_class = serializers.UserSerializer

    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            password = hashlib.md5(body['password'].encode()).hexdigest()

            user = User.objects.filter(username=username, password=password)

            if user.count() > 0:
                return Response({"id": user[0].id,
                                 "username": user[0].username,
                                 "email": user[0].email,
                                 "name": user[0].name,
                                 "role": user[0].user_role},
                                status=status.HTTP_200_OK)

            return Response("null", status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        except:
            return Response("Bad Request",
                            status=status.HTTP_400_BAD_REQUEST)


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.select_related('church').prefetch_related("church__shepherd").all()
    serializer_class = serializers.PersonSerializer
    pagination_class = paginations.StandardResultsSetPaginationLevelHighest
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'first_name', 'last_name', 'church_id', 'identification']
    search_fields = ['first_name', 'last_name', 'full_name', 'identification']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.PersonAddUpdateSerializer
        return serializers.PersonSerializer


class ChurchViewSet(ModelViewSet):
    queryset = Church.objects.select_related("shepherd").select_related("created_by").all()
    serializer_class = serializers.ChurchSerializer
    pagination_class = paginations.StandardResultsSetPaginationLevelHighest
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'global_title', 'local_title', 'shepherd']
    search_fields = ['global_title',]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.ChurchAddUpdateSerializer
        return serializers.ChurchSerializer