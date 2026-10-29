from django.contrib import admin

from .models import Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'puesto', 'microbiologia', 'bacteriologia', 'quimica', 'valor_total')
    list_filter = ('puesto',)
