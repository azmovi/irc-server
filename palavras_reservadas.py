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
    multipla_mensagem = False

    return msg, conexoes, mensagem_valida, multipla_mensagem


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
    multipla_mensagem = False
    conexoes = [conexao]

    return msg, conexoes, mensagem_valida, multipla_mensagem


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
    multipla_mensagem = False
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

    return msg, conexoes, mensagem_valida, multipla_mensagem


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
    conexao.lista_de_canais_atuais.append(nome_canal)

    canal_existe = servidor.canais.get(nome_canal_upper)

    if canal_existe:
        servidor.canais[nome_canal_upper].append(conexao.nome)

    else:
        servidor.canais[nome_canal_upper] = [conexao.nome]

    mensagem_valida = True
    msg = b':%s JOIN :%s\r\n' % (conexao.nome, nome_canal)

    nome_dos_usuarios_em_um_canal = servidor.canais.get(nome_canal_upper)

    conexoes = [
        servidor.users.get(nome_usuario.upper()) for nome_usuario in nome_dos_usuarios_em_um_canal
    ]


    string_dos_usuarios_ordenados = b' '.join(sorted(nome_dos_usuarios_em_um_canal))

    multipla_mensagem = b':server 353 %s = %s :%s\r\n' % (conexao.nome, nome_canal, string_dos_usuarios_ordenados)
    multipla_mensagem += b':server 366 %s %s :End of /NAMES list.\r\n' % (conexao.nome, nome_canal)

    return msg, conexoes, mensagem_valida, multipla_mensagem


def retornar_saida_no_canal(
    conexao: Conexao, tokens: list[bytes], servidor: Servidor
) -> tuple[bytes, list[Conexao], bool]:
    """
    Remove um usuario de um determinado canal
    """

    conexoes = []
    mensagem_valida = False
    canal = tokens[0]
    multipla_mensagem = False

    if len(tokens) == 1:   # passou mais de um paramentro
        canal = canal[:-2]

    nome_dos_usuarios_em_um_canal = servidor.canais[canal.upper()]

    if conexao.nome in nome_dos_usuarios_em_um_canal:
        for nome_usuario in nome_dos_usuarios_em_um_canal:
            conexoes.append(servidor.users.get(nome_usuario.upper()))

        servidor.canais[canal.upper()].remove(conexao.nome)
        conexao.lista_de_canais_atuais.remove(canal)

        msg = b':%s PART %s\r\n' % (conexao.nome, canal)
        mensagem_valida = True

    return msg, conexoes, mensagem_valida, multipla_mensagem

