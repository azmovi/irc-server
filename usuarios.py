import re


def validar_nome(nome: bytes) -> bool:
    """
    Função responsável por validar o nome do usuário usando regex.

    Return:
        Um booleano baseado se o nick do usuário é falso ou verdadeiro
    """
    return re.match(rb'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None


def tratar_nome(tokens: list[bytes]) -> bytes:
    """
    Função responsável por tratar o nick passado pelo usuario removendo o '\r\n',
    além de verificar se esse nick não esta presente no nosso "banco de dados"
    de nick.

    Return:
        retorna o nick tratado do usuario e um booleano validando se ninguem ja registrou
        esse nick
    """
    nome = b''.join(tokens)
    nome_tratado = nome[:-2]

    return nome_tratado


def validar_usuario(tokens: list[bytes], servidor, conexao) -> bytes:
    """
    Verifica qual resposta o servidor deve responder ao usuario baseado no nick
    que ele colocou.

    Return:
        retorna a mensagem que deve ser enviada pelo serviador.
    """
    resposta = b''
    nome_novo = tratar_nome(tokens)
    nome_valido = validar_nome(nome_novo)

    if nome_valido:
        nome_uppercase = nome_novo.upper()

        if not servidor.users.get(nome_uppercase):
            if conexao.nome == b'*':   # Cria ususario
                resposta = b':server 001 %s :Welcome\r\n' % nome_novo
                resposta += (
                    b':server 422 %s :MOTD File is missing\r\n' % nome_novo
                )

            else:   # Trocar de nome
                resposta = b':%s NICK %s\r\n' % (conexao.nome, nome_novo)

            servidor.users[nome_uppercase] = conexao
            conexao.nome = nome_novo

        else:   # Nome ja existe
            resposta = b':server 433 %s %s :Nickname is already in use\r\n' % (
                conexao.nome,
                nome_novo,
            )

    else:   # Nome invalido
        resposta = b':server 432 %s %s :Erroneous nickname\r\n' % (
            conexao.nome,
            nome_novo,
        )

    return resposta
