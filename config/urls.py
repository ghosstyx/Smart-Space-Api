from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('auth/', include('accounts.urls', namespace='accounts')),
    path('org/', include('organizations.urls', namespace='organizations')),
    # path('user/', include('user_profiles.urls', namespace='user_profiles')),
    # path('organizations/', include('organizations.urls', namespace='organizations')),
]

# Schema URLs
urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Media Assets and Statics
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
