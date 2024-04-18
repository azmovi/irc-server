def retornar_mensagem_de_ping(tokens: list[bytes]) -> bytes:
    msg = b':server PONG server :' + b' '.join(tokens)
    return msg
