from django.contrib import admin
from pagina_inicial.models import Reclame, Aviso
from plataforma.models import OperadoresAviso

admin.site.register(Reclame)
admin.site.register(Aviso)
admin.site.register(OperadoresAviso)