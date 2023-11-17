from django.contrib import admin
from pagina_inicial.models import Reclame, Aviso, Contato
from plataforma.models import OperadoresAviso

admin.site.register(Reclame)
admin.site.register(Aviso)
admin.site.register(OperadoresAviso)
admin.site.register(Contato)