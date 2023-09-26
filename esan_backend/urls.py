from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="EsAN API",
      default_version='v1',
      description="EsAN",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('api/', include('home.urls')),
    path('api/', include('account.urls')),
    path('api/', include('tournament.urls')),
    path('api/', include('faq.urls')),
    path('api/', include('testimonial.urls')),
    path('api/', include('our_team.urls')),
    path('api/', include('newsletter.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
