from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from plataforma import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pagina_inicial.urls')),
    path('', include('eta.urls')),
    path('', include('operadores.urls')),
    path('', include('plataforma.urls')),
    path('', include('laboratorio.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
