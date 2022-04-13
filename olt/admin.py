from django.contrib import admin

from olt.models import (SistemaOltModels, SistemaOnuModels, SistemaPonModels,
                        SistemaSlotModels, SMNPOltModels)

# Register your models here.


@admin.register(SistemaOltModels)
class SistemaOltModelsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ip', 'porta', 'usuario', 'senha', 'smnp', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'ip', 'porta', 'usuario', 'senha', 'smnp')


@admin.register(SMNPOltModels)
class SMNPOltModelsAdmin(admin.ModelAdmin):
    list_display = ('community', 'version', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('community', 'version')


@admin.register(SistemaSlotModels)
class SistemaSlotModelsAdmin(admin.ModelAdmin):
    list_display = ('slot', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('slot',)


@admin.register(SistemaPonModels)
class SistemaPonModelsAdmin(admin.ModelAdmin):
    list_display = ('pon', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('pon',)


@admin.register(SistemaOnuModels)
class SistemaOnuModelsAdmin(admin.ModelAdmin):
    list_display = ('onu', 'fhtt', 'descricao', 'cliente', 'ativo')
    list_filter = ('ativo', 'contrato')
    search_fields = ('onu',)
