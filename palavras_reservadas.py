import re

USERS = set()


def retornar_mensagem_de_ping(tokens: list[bytes]) -> bytes:
    """
    Função responsável pela reposta do servidor após chamada da palavra reservada PING.

    Return:
        A resposta do servidor para a palavra reservada PING
    """
    msg = b':server PONG server :' + b' '.join(tokens)
    return msg


def validar_nome(nome: bytes) -> bool:
    """
    Função responsável por validar o nome do usuário usando regex.

    Return:
        Um booleano baseado se o nick do usuário é falso ou verdadeiro
    """
    return re.match(rb'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


def retornar_mensagem_de_nick(tokens: list[bytes]) -> bytes:
    """
    Função responsável pela resposta do servidor após chamada da palavra NICK.

    Return:
        A resposta do servidor para a palavra reservada NICK
    """
    nick = b''.join(tokens)
    nick_tratado = nick[:-2]
    resposta = b''

    if validar_nome(nick_tratado):
        resposta = b':server 001 %s :Welcome\r\n' % nick_tratado
        resposta += b':server 422 %s :MOTD File is missing\r\n' % nick_tratado

    else:
        resposta = b':server 432 * %s :Erroneous nickname\r\n' % nick_tratado

    return resposta
