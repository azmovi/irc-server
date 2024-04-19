#!/usr/bin/env python3
import asyncio
from grader.tcp import Servidor
from trata_dados import enviar_dados_tratados

setattr(Servidor, 'users', set())

def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()


def dados_recebidos(conexao, dados, servidor):
    if dados == b'':
        return sair(conexao)

    print(servidor.users)
    enviar_dados_tratados(conexao, dados, servidor)


def conexao_aceita(conexao):
    print(conexao, 'nova conexão')
    conexao.registrar_recebedor(dados_recebidos)


servidor = Servidor(6667)
servidor.registrar_monitor_de_conexoes_aceitas(conexao_aceita)
asyncio.get_event_loop().run_forever()
