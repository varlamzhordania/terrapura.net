"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls.i18n import i18n_patterns # Wrap whole urls patterns to add translation to all urls

# from .views import set_language

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', include('account.urls', namespace='account')),
    path('', include('main.urls', namespace='main')),
    path('', include('herbs.urls', namespace='herbs')),
    path('', include('partners.urls', namespace='partners')),
    path('', include('inventory.urls', namespace='inventory')),
    path('', include('checkout.urls', namespace='checkout')),
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),

]

urlpatterns += [
    # path("setlang/", set_language, name="set_language"),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # re_path(r'^rosetta/', include('rosetta.urls')),
    path('hijack/', include('hijack.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]


urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
