from usuarios import validar_usuario

def retornar_mensagem_de_ping(tokens: list[bytes], _) -> bytes:
    """
    Função responsável pela reposta do servidor após chamada da palavra reservada PING.

    Return:
        A resposta do servidor para a palavra reservada PING
    """
    msg = b':server PONG server :' + b' '.join(tokens)
    return msg


def retornar_mensagem_de_nick(tokens: list[bytes], servidor) -> bytes:
    """
    Função responsável pela resposta do servidor após chamada da palavra NICK.

    Return:
        A resposta do servidor para a palavra reservada NICK
    """
    msg = validar_usuario(tokens, servidor)
    return msg
