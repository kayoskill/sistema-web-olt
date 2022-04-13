from django.contrib import admin

from banco.models import BancoHubsoftModels

# Register your models here.


@admin.register(BancoHubsoftModels)
class BancoHubsoftModelsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ip', 'porta', 'usuario', 'senha', 'base', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'ip', 'porta', 'usuario', 'senha', 'base')
