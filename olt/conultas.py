import psycopg2
from banco.models import BancoHubsoftModels
from django.shortcuts import get_object_or_404
from easysnmp import Session

from olt.models import SistemaOltModels


class BancoHubsoft():
    def __init__(self) -> None:
        try:
            banco = get_object_or_404(BancoHubsoftModels, ativo=True)
            self.bd = psycopg2.connect(host=banco.ip, database=banco.base, user=banco.usuario,
                                       password=banco.senha, port=banco.porta)
        except:
            raise Exception('Erro ao conectar ao banco de dados')

    def select_cpe(self, fhtt):
        dicionario = {}
        cursor = self.bd.cursor()

        cursor.execute(
            f"select c2.nome_razaosocial ,c.descricao ,ss.descricao,c.params from cpe c inner join cliente_servico_autenticacao_cpe csac on csac.id_cpe = c.id_cpe inner join cliente_servico_autenticacao csa on csa.id_cliente_servico_autenticacao = csac.id_cliente_servico_autenticacao inner join cliente_servico cs on cs.id_cliente_servico = csa.id_cliente_servico inner join servico_status ss on ss.id_servico_status = cs.id_servico_status inner join cliente c2 on c2.id_cliente = cs.id_cliente where c.phy_addr = '{fhtt}'")
        resultado = cursor.fetchall()
        for dado in resultado:
            if dado:
                dicionario.update(
                    {'fhtt': fhtt, 'cliente': dado[0], 'descricao': dado[1], 'contrato': dado[2]})
            return dicionario
        if len(resultado) == 0:
            cursor2 = self.bd.cursor()
            cursor2.execute(
                f"select c.descricao from cpe c where c.phy_addr = '{fhtt}'")
            resultado2 = cursor2.fetchall()
            if resultado2:
                for dado in resultado2:

                    if dado:
                        dicionario.update(
                            {'fhtt': fhtt, 'cliente': '****', 'descricao': dado[0], 'contrato': '****'})
            else:
                dicionario.update(
                    {'fhtt': fhtt, 'cliente': 'INATIVO', 'descricao': 'INATIVO', 'contrato': 'INATIVO'})
            return dicionario


class ConexaoSmnp():
    def __init__(self, id_olt) -> None:
        try:
            _ip = get_object_or_404(SistemaOltModels, ativo=True, id=id_olt)
            self.snmp = Session(
                hostname=_ip.ip, community=_ip.smnp.community, version=int(_ip.smnp.version))
        except Exception as e:
            raise Exception(f'Erro ao conectar ao olt, {e}')

    def listar_olt(self):
        try:
            dicionario = self.snmp.bulkwalk(
                '1.3.6.1.4.1.5875.800.3.10.1.1.4')
            if dicionario:
                salvar = {}
                for dados in dicionario:
                    onu = dados.value
                    codigo = dados.oid
                    codigo = codigo.split('.')[-1]

                    slotpon = self.snmp.get(
                        f'1.3.6.1.4.1.5875.800.3.9.3.4.1.2.{str(codigo)}')
                    slotpon = slotpon.value
                    slotpon = slotpon.replace('PON', '')
                    slotpon = slotpon.split('/')

                    salvar.update(
                        {codigo: {'slot': int(slotpon[0]), 'pon': int(slotpon[1]), 'onu': int(onu)}})

                return salvar
        except:
            return False

    def listar_pons(self):
        try:
            dicionario = self.snmp.bulkwalk(
                '1.3.6.1.4.1.5875.800.3.9.3.4.1.2', max_repetitions=100)
            if dicionario:
                salvar = {}
                for dados in dicionario:
                    slotpon = dados.value
                    slotpon = slotpon.replace('PON', '')
                    slotpon = slotpon.split('/')
                    codigo = dados.oid
                    codigo = codigo.split('.')[-1]
                    salvar.update(
                        {codigo: {'slot': slotpon[0], 'pon': slotpon[1]}})

                return salvar
        except:
            return False

    def listar_sinal(self, codigo):
        try:
            sinal = self.snmp.get(
                f'1.3.6.1.4.1.5875.800.3.9.3.3.1.6.{str(codigo)}')
            sinal = sinal.value
            if (len(sinal)) > 0:
                sinal = f"{sinal[0:3]}.{sinal[3:]}"
            else:
                sinal = -60.00

            return float(sinal)
        except:
            return False

    def listar_fhtt(self, codigo):
        fhtt = self.snmp.get(
            f'1.3.6.1.4.1.5875.800.3.10.1.1.10.{str(codigo)}')
        return str(fhtt.value)

    def lista_autenticados(self, codigo):
        try:
            auth = self.snmp.get(
                f'1.3.6.1.4.1.5875.800.3.9.3.4.1.12.{str(codigo)}')
            cd = auth.value
            return cd
        except:
            return False

    def listar_status(self, codigo):
        try:
            status = self.snmp.get(
                f'1.3.6.1.4.1.5875.800.3.10.1.1.11.{str(codigo)}')
            cd = status.value
            if int(cd) == 1:
                return 'ON'
            else:
                return 'OFF'
        except:
            return 'UNT'
