from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('api/', include('home.urls')),
    path('api/', include('account.urls')),
    path('api/', include('tournament.urls')),
    path('api/', include('faq.urls')),
    path('api/', include('testimonial.urls')),
    path('api/', include('our_team.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
