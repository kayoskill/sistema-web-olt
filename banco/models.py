from django.db import models

# Create your models here.


class BancoHubsoftModels(models.Model):
    nome = models.CharField(('Nome'), max_length=100, unique=True)
    ip = models.CharField(('Host'), max_length=100, unique=True)
    porta = models.CharField(('Porta'), max_length=100)
    usuario = models.CharField(('Usuario'), max_length=100)
    senha = models.CharField(('Senha'), max_length=100)
    base = models.CharField(('Base'), max_length=100)
    ativo = models.BooleanField(("Ativo"), default=True)

    class Meta:
        managed = True
        verbose_name = 'Banco Hubsoft'
        verbose_name_plural = 'Banco Hubsoft'

    def __str__(self):
        return self.nome
