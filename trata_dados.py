from grader.tcp import Conexao
from palavras_reservadas import retornar_mensagem_de_ping, verificar_nick


# Criando o atributo novo chamado residuos
setattr(Conexao, 'residuos', b'')


PALAVRAS_RESERVADAS = {
    b'PING': retornar_mensagem_de_ping,
    b'NICK': verificar_nick,
}

def enviar_dados_tratados(conexao: Conexao, dados: bytes) -> None:
    lista_de_mensagens = tratar_residuo(conexao, dados)
    for mensagem in lista_de_mensagens:
        try:
            resposta = tratar_mensagem(mensagem)
            conexao.enviar(resposta)
        except KeyError:
            conexao.enviar(b'')


def dividir_dados_em_mensagens_e_residuos(
    dados: bytes,
) -> tuple[list[bytes], bytes]:

    lista = []
    string = b''

    for byte in dados:
        string += bytes([byte])
        if chr(byte) == '\n':
            lista.append(string)
            string = b''

    residuo = string

    return lista, residuo


def tratar_mensagem(mensagem: bytes) -> bytes:
    palavra_reservada, *conteudo_da_mensagem = mensagem.split(b' ', 1)
    resposta = PALAVRAS_RESERVADAS[palavra_reservada](
        conteudo_da_mensagem
    )

    return resposta


def tratar_residuo(conexao: Conexao, dados: bytes) -> list[bytes]:
    dados_com_residuo = conexao.residuos + dados
    conexao.residuos = b''

    lista_de_mensagens, residuos = dividir_dados_em_mensagens_e_residuos(
        dados_com_residuo
    )

    conexao.residuos = residuos

    return lista_de_mensagens
