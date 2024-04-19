import re


def validar_nome(nome: bytes) -> bool:
    """
    Função responsável por validar o nome do usuário usando regex.

    Return:
        Um booleano baseado se o nick do usuário é falso ou verdadeiro
    """
    return re.match(rb'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


def tratar_nick(tokens: list[bytes]) -> tuple[bytes, bool] :
    """
    Função responsável por tratar o nick passado pelo usuario removendo o '\r\n',
    além de verificar se esse nick não esta presente no nosso "banco de dados"
    de nick.

    Return:
        retorna o nick tratado do usuario e um booleano validando se ninguem ja registrou
        esse nick
    """
    nick = b''.join(tokens)
    nick_tratado = nick[:-2]

    nick_valido = validar_nome(nick_tratado)

    return nick_tratado, nick_valido


def validar_usuario(tokens: list[bytes], servidor) -> bytes:
    """
    Verifica qual resposta o servidor deve responder ao usuario baseado no nick
    que ele colocou

    Return:
        retorna a mensagem que deve ser enviada pelo serviador.
    """
    nick, nick_valido = tratar_nick(tokens)
    resposta = b''

    if nick_valido:
        nick_uppercase = nick.upper()
        if nick_uppercase not in servidor.users:
            resposta = b':server 001 %s :Welcome\r\n' % nick
            resposta += b':server 422 %s :MOTD File is missing\r\n' % nick

        else:
            resposta = b':server 433 * %s :Nickname is already in use' % nick
            servidor.users.add(nick_uppercase)
    else:
        resposta = b':server 432 * %s :Erroneous nickname\r\n' % nick

    return resposta
