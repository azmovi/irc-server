import re

from grader.tcp import Conexao, Servidor


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


def validar_usuario(
    conexao: Conexao, tokens: list[bytes], servidor: Servidor
) -> bytes:
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
        if not existe_usuario(servidor, nome_novo):

            if conexao.nome == b'*':
                resposta = criar_usuario(nome_novo)

            else:
                resposta = trocar_nome(conexao, nome_novo, servidor)

            servidor.users[nome_novo.upper()] = conexao
            conexao.nome = nome_novo

        else:
            resposta = b':server 433 %s %s :Nickname is already in use\r\n' % (
                conexao.nome,
                nome_novo,
            )
    else:
        resposta = b':server 432 %s %s :Erroneous nickname\r\n' % (
            conexao.nome,
            nome_novo,
        )

    return resposta


def existe_usuario(servidor: Servidor, nome_novo: bytes) -> bool:
    """
    Verificar se existe usuario presente na base de usuarios.
    """
    return servidor.users.get(nome_novo.upper())


def criar_usuario(nome_novo: bytes) -> bytes:
    """
    Cria mensagem de usuario criado.
    """
    resposta = b':server 001 %s :Welcome\r\n' % nome_novo
    resposta += b':server 422 %s :MOTD File is missing\r\n' % nome_novo

    return resposta


def trocar_nome(conexao, nome_novo, servidor) -> bytes:
    """
    Troca o nome do usuario e remove o antigo da base de usuarios.
    """
    resposta = b':%s NICK %s\r\n' % (conexao.nome, nome_novo)
    del servidor.users[conexao.nome.upper()]

    return resposta
