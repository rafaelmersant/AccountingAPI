# Django
from django.urls import include, path, re_path

# Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views

router = DefaultRouter()
router.register('concepts', views.ConceptViewSet)
router.register('users', views.UserViewSet)
router.register('people', views.PersonViewSet)
router.register('churches', views.ChurchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/login/$', views.UserLogin.as_view(), name='UserLogin'),
]
