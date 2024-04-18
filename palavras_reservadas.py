import re

USERS = set()


def retornar_mensagem_de_ping(tokens: list[bytes]) -> list[bytes]:
    msg = b':server PONG server :' + b' '.join(tokens)
    return msg

def validar_nome(nome):
    return re.match(rb'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None

def verificar_nick(tokens: list[bytes]) -> bytes:
    nick = b''.join(tokens)
    nick_tratado = nick[:-2]
    resposta = b''

    if validar_nome(nick_tratado):
        resposta = b':server 001 %s :Welcome\r\n' % nick_tratado
        resposta += b':server 422 %s :MOTD File is missing\r\n' % nick_tratado
    else:
        resposta = b':server 432 * %s :Erroneous nickname\r\n' % nick_tratado

    return resposta 
