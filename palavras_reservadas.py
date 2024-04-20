from usuarios import validar_usuario
from grader.tcp import Servidor, Conexao


def retornar_mensagem_de_ping(tokens: list[bytes], *_) -> bytes:
    """
    Função responsável pela reposta do servidor após chamada da palavra reservada PING.

    Return:
        A resposta do servidor para a palavra reservada PING
    """
    msg = b':server PONG server :' + b''.join(tokens)
    return msg


def retornar_mensagem_de_nick(
    tokens: list[bytes],
    servidor: Servidor,
    conexao: Conexao
) -> bytes:
    """
    Função responsável pela resposta do servidor após chamada da palavra NICK.

    Return:
        A resposta do servidor para a palavra reservada NICK
    """
    msg = validar_usuario(tokens, servidor, conexao)
    return msg


def retornar_mensagem_privada(
    tokens: list[bytes],
    servidor: Servidor,
    conexao: Conexao
) -> bytes:
    """
    Example:
        >>> PRIVMS destinatario :mensagem
        :remetente PRIVMSG destinatario :mensagem

    """
    destinatario = tokens[0]
    conteudo = b''.join(tokens[1:])
    msg = b''

    conexao_destinatario = servidor.users.get(destinatario.upper())
    if (conexao_destinatario):
        msg = b':%s PRIVMSG %s %s' % (
            conexao.nome, conexao_destinatario.nome, conteudo
        )
    return msg

