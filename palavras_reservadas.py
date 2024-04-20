from usuarios import validar_usuario
from grader.tcp import Servidor, Conexao


def retornar_mensagem_de_ping(conexao: Conexao, tokens: list[bytes], _) -> tuple[bytes, Conexao, bool]:
    """
    Função responsável pela reposta do servidor após chamada da palavra reservada PING.

    Return:
        A resposta do servidor para a palavra reservada PING
    """
    msg = b':server PONG server :' + b''.join(tokens)
    mensagem_valida = True
    return msg, conexao, mensagem_valida


def retornar_mensagem_de_nick(
    conexao: Conexao,
    tokens: list[bytes],
    servidor: Servidor,
) -> tuple[bytes, Conexao, bool]:
    """
    Função responsável pela resposta do servidor após chamada da palavra NICK.

    Return:
        A resposta do servidor para a palavra reservada NICK
    """
    msg = validar_usuario(conexao, tokens, servidor)
    mensagem_valida = True
    return msg, conexao, mensagem_valida


def retornar_mensagem_privada(
    conexao: Conexao,
    tokens: list[bytes],
    servidor: Servidor
) -> tuple[bytes, Conexao, bool]:
    """
    Example:
        >>> PRIVMS destinatario :mensagem
        :remetente PRIVMSG destinatario :mensagem

    """
    destinatario = tokens[0]
    conteudo = b''.join(tokens[1:])
    mensagem_valida = False
    msg = b''

    conexao_destinatario = servidor.users.get(destinatario.upper())

    if (conexao_destinatario):
        msg = b':%s PRIVMSG %s %s' % (
            conexao.nome, conexao_destinatario.nome, conteudo
        )
        mensagem_valida = True

    return msg, conexao_destinatario, mensagem_valida


