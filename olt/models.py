from django.db import models

# Create your models here.


class SMNPOltModels(models.Model):
    community = models.CharField(('Community'), max_length=100)
    version = models.CharField(('Version'), max_length=100)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'SMNP Olt'
        verbose_name_plural = 'SMNP Olt'

    def __str__(self) -> str:
        return self.community


class SistemaOltModels(models.Model):
    nome = models.CharField(('Nome'), max_length=100, unique=True)
    ip = models.CharField(('Host'), max_length=100, unique=True)
    porta = models.CharField(('Porta'), max_length=100)
    usuario = models.CharField(('Usuario'), max_length=100)
    senha = models.CharField(('Senha'), max_length=100)
    smnp = models.ForeignKey(
        SMNPOltModels, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'Sistema Olt'
        verbose_name_plural = 'Sistema Olt'

    def __str__(self):
        return self.nome


class SistemaSlotModels(models.Model):
    slot = models.IntegerField(('SLOT'), default=0)
    olt = models.ManyToManyField(SistemaOltModels)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'Sistema Slot'
        verbose_name_plural = 'Sistema Slot'

    def __str__(self):
        return self.slot


class SistemaPonModels(models.Model):
    codigo = models.CharField(('Codigo'), max_length=100, unique=True)
    pon = models.IntegerField(('PON'), default=0)
    slot = models.ManyToManyField(SistemaSlotModels)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'Sistema Pon'
        verbose_name_plural = 'Sistema Pon'

    def __str__(self):
        return self.pon


class SistemaOnuModels(models.Model):
    onu = models.IntegerField(('ONU'), default=0)
    codigo = models.CharField(('Codigo'), max_length=100, unique=True)
    vlan = models.IntegerField(('Vlan'), default=0)
    pon = models.ManyToManyField(SistemaPonModels)
    fhtt = models.CharField(('FHTT'), max_length=100)
    descricao = models.CharField(('Descricao'), max_length=100)
    sinal = models.CharField(('Sinal'), max_length=100)
    status = models.CharField(('Status'), max_length=100)
    cliente = models.CharField(('Cliente'), max_length=100)
    contrato = models.CharField(('Contrato'), max_length=100)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'Sistema Onu'
        verbose_name_plural = 'Sistema Onu'

    def __str__(self):
        return self.onu
