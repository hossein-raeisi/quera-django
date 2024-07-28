from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf/', include('Quera.drf.urls')),
    path('async/', include('Quera.async_app.urls')),
    path('celery/', include('Quera.celery_app.urls')),
]
