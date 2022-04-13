from django.shortcuts import render

from olt.conultas import ConexaoSmnp

# Create your views here.


def home_olt(request):
    conexao = ConexaoSmnp(1)
    conexao.listar_olt()
    return render(request, 'olt/home_olt.html')
