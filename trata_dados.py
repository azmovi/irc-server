from grader.tcp import Conexao
from palavras_reservadas import retornar_mensagem_de_ping, retornar_mensagem_de_nick


# Criando o atributo novo chamado resíduos
setattr(Conexao, 'residuos', b'')


PALAVRAS_RESERVADAS = {
    b'PING': retornar_mensagem_de_ping,
    b'NICK': retornar_mensagem_de_nick,
}


def enviar_dados_tratados(conexao: Conexao, dados: bytes) -> None:
    """
    Função responsável por receber as mensagens dos usuários e garantir que 
    o servidor responda de forma correta
    """
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
    """
    Função responsável por dividir os dados em mensagens completas terminadas por '\n'
    e guardar o resíduo, no caso dados que não terminam em '\n'.

    Return:
        Uma tupla contendo a lista de mensagem dos usuários separadas pelo '\n'
        e a mensagem residual.
    """

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
    """
    Função responsável por dividir a mensagem do usuários em palavra reservada e
    o conteúdo propriamente dito da mensagem, além de executar a função respectiva
    a essa palavra reservada.

    Return:
        Retorna a resposta do servidor dado uma palavra reservada e o restante do 
        conteúdo do usuário.
    """
    palavra_reservada, *conteudo_da_mensagem = mensagem.split(b' ', 1)
    resposta = PALAVRAS_RESERVADAS[palavra_reservada](conteudo_da_mensagem)

    return resposta


def tratar_residuo(conexao: Conexao, dados: bytes) -> list[bytes]:
    """
    Função responsável por tratar a mensagem do usuários e verificar se nela contém
    algum tipo de resíduo (não termina em '\n'), caso apresente é armazenado em um
    atributo da classe Conexao.

    Return:
        Retorna uma lista de mensagens divididas por usuário.
    """
    dados_com_residuo = conexao.residuos + dados
    conexao.residuos = b''

    lista_de_mensagens, residuos = dividir_dados_em_mensagens_e_residuos(
        dados_com_residuo
    )

    conexao.residuos = residuos

    return lista_de_mensagens
