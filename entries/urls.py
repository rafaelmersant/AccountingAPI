# Django
from cgitb import lookup
from django.urls import include, path, re_path

from rest_framework_nested import routers

# Views
from . import views

router = routers.DefaultRouter()
router.register('entries', views.EntryViewSet)

entries_router = routers.NestedDefaultRouter(router, 'entries', lookup='entry')
entries_router.register('items', views.EntryItemViewSet, basename='entry-items')

urlpatterns = router.urls + entries_router.urls
