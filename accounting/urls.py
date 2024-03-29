import debug_toolbar
from django.conf import settings
from django.contrib import admin
from rest_framework.authtoken import views
# from rest_framework_simplejwt import views as jwt_views

from django.urls import include, path, re_path

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^api/v1/', include('administration.urls')),
    re_path(r'^api/v1/', include('entries.urls')),
    re_path(r'^api/v1/auth', include('rest_framework.urls')),
    # re_path(r'^api/v1/token/', jwt_views.TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'),
    # re_path(r'^api/v1/token/refresh/',
    #     jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('__debug__/', include('debug_toolbar.urls')),
]
