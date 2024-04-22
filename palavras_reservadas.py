from usuarios import validar_usuario
from grader.tcp import Servidor, Conexao


def retornar_mensagem_de_ping(
    conexao: Conexao, tokens: list[bytes], _
) -> tuple[bytes, list[Conexao], bool]:
    """
    Função responsável pela reposta do servidor após chamada da palavra reservada PING.

    Return:
        A resposta do servidor para a palavra reservada PING
    """
    msg = b':server PONG server :' + b''.join(tokens)
    mensagem_valida = True
    conexoes = [conexao]

    return msg, conexoes, mensagem_valida


def retornar_mensagem_de_nick(
    conexao: Conexao,
    tokens: list[bytes],
    servidor: Servidor,
) -> tuple[bytes, list[Conexao], bool]:
    """
    Função responsável pela resposta do servidor após chamada da palavra NICK.

    Return:
        A resposta do servidor para a palavra reservada NICK
    """
    msg = validar_usuario(conexao, tokens, servidor)
    mensagem_valida = True
    conexoes = [conexao]

    return msg, conexoes, mensagem_valida


def retornar_mensagem_privada(
    conexao: Conexao, tokens: list[bytes], servidor: Servidor
) -> tuple[bytes, list[Conexao], bool]:
    """
    Example:
        >>> PRIVMSG destinatario :mensagem
        :remetente PRIVMSG destinatario :mensagem

        >>> PRIVMSG #canal :mensagem
        :remetente PRIVMSG #canal :mensagem

    """
    meio = tokens[0]
    conteudo = b''.join(tokens[1:])
    mensagem_valida = False
    msg = b''
    conexoes = []

    if (b'%c' % meio[0]) == b'#':   # canal

        canal = meio
        users_no_canal = servidor.canais.get(canal.upper())

        if users_no_canal:
            msg = b':%s PRIVMSG %s %s' % (conexao.nome, canal, conteudo)

            mensagem_valida = True
            for user in users_no_canal:
                if user != conexao.nome:
                    conexoes.append(servidor.users[user.upper()])

    else:   # usuario
        destinatario = meio
        conexao_destinatario = servidor.users.get(destinatario.upper())

        if conexao_destinatario:
            msg = b':%s PRIVMSG %s %s' % (
                conexao.nome,
                conexao_destinatario.nome,
                conteudo,
            )

            mensagem_valida = True

        conexoes = [conexao_destinatario]

    return msg, conexoes, mensagem_valida


def retornar_entrou_no_canal(
    conexao: Conexao, tokens: list[bytes], servidor: Servidor
) -> tuple[bytes, list[Conexao], bool]:
    """
    Retorna mensagem que o usuario entrou no canal espefico
    Example:
        >>>JOIN #canal1
        nick JOIN #canal1
    """
    nome_canal = b''.join(tokens)[:-2]
    nome_canal_upper = nome_canal.upper()

    canal_existe = servidor.canais.get(nome_canal_upper)

    if canal_existe:
        servidor.canais[nome_canal_upper].append(conexao.nome)

    else:
        servidor.canais[nome_canal_upper] = [conexao.nome]

    mensagem_valida = True
    msg = b':%s JOIN :%s\r\n' % (conexao.nome, nome_canal)

    conexoes = [conexao]

    return msg, conexoes, mensagem_valida


def retornar_saida_no_canal(
    conexao: Conexao, tokens: list[bytes], servidor: Servidor
) -> tuple[bytes, list[Conexao], bool]:
    """
    Remove um usuario de um determinado canal
    """

    conexoes = []
    mensagem_valida = False
    canal = tokens[0]

    if len(tokens) == 1:   # passou mais de um paramentro
        canal = canal[:-2]

    nome_dos_usuarios_em_um_canal = servidor.canais[canal.upper()]

    if conexao.nome in nome_dos_usuarios_em_um_canal:
        for nome_usuario in nome_dos_usuarios_em_um_canal:
            conexoes.append(servidor.users.get(nome_usuario.upper()))

        servidor.canais[canal.upper()].remove(conexao.nome)

        msg = b':%s PART %s\r\n' % (conexao.nome, canal)
        mensagem_valida = True

    return msg, conexoes, mensagem_valida
