# Django
from django.urls import include, path, re_path

# Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views

router = DefaultRouter()
# router.register('entries', views.EntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
