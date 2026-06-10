import os as sistema_operacional
import sys as sistema
import time as tempo
import json as formato_json
from datetime import datetime as data_e_hora

DIRETORIO_BASE = (
    sistema_operacional.path.dirname(sistema.executable)
    if getattr(sistema, "frozen", False)
    else sistema_operacional.path.dirname(
        sistema_operacional.path.dirname(
            sistema_operacional.path.abspath(__file__)
        )
    )
)
CAMINHO_BANCO = sistema_operacional.path.join(DIRETORIO_BASE, "log.dat")

def limpar_tela():
    sistema_operacional.system("cls")
    
def aguarde(segundos):
    tempo.sleep(segundos)
    
def inicializar_banco_de_dados():
    if not sistema_operacional.path.exists(CAMINHO_BANCO):
        print("Banco de Dados Inexistente. Criando...")
        with open(CAMINHO_BANCO, "w", encoding="utf-8"):
            pass
        return

    registros = ler_registros()
    with open(CAMINHO_BANCO, "r", encoding="utf-8") as banco:
        dados = banco.read().strip()

    if dados.startswith("{"):
        salvar_registros(registros)


def separar_data_hora(data_hora):
    if " às " in data_hora:
        data, hora = data_hora.split(" às ", 1)
        if len(hora.split(":")) == 2:
            hora += ":00"
        return data, hora
    return data_hora, "00:00:00"


def ler_registros():
    if not sistema_operacional.path.exists(CAMINHO_BANCO):
        return []

    with open(CAMINHO_BANCO, "r", encoding="utf-8") as banco:
        dados = banco.read().strip()

    if not dados:
        return []

    if dados.startswith("{"):
        dados_antigos = formato_json.loads(dados)
        registros = []
        for nome, informacoes in dados_antigos.items():
            data, hora = separar_data_hora(informacoes[1])
            registros.append(
                {
                    "nome": nome.strip(),
                    "pontos": int(informacoes[0]),
                    "data": data,
                    "hora": hora,
                }
            )
        return registros

    registros = []
    for bloco in dados.split("\n\n"):
        campos = {}
        for linha in bloco.splitlines():
            campo, separador, valor = linha.partition(":")
            if separador:
                campos[campo.strip()] = valor.strip()

        if "Nome" in campos and "Pontuação" in campos:
            registros.append(
                {
                    "nome": campos["Nome"],
                    "pontos": int(campos["Pontuação"]),
                    "data": campos.get("Data", ""),
                    "hora": campos.get("Hora", ""),
                }
            )
    return registros


def salvar_registros(registros):
    blocos = []
    for registro in registros:
        blocos.append(
            "\n".join(
                (
                    f"Nome: {registro['nome']}",
                    f"Pontuação: {registro['pontos']}",
                    f"Data: {registro['data']}",
                    f"Hora: {registro['hora']}",
                )
            )
        )

    with open(CAMINHO_BANCO, "w", encoding="utf-8") as banco:
        banco.write("\n\n".join(blocos))
        if blocos:
            banco.write("\n")
    
def escrever_dados(nome, pontos):
    agora = data_e_hora.now()
    registros = ler_registros()
    registros.append(
        {
            "nome": nome.replace("\n", " ").strip(),
            "pontos": pontos,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M:%S"),
        }
    )
    salvar_registros(registros)
    
def maior_pontuador():
    nome_maior = None
    data_jogada = None
    maior_pontos = -1

    for registro in ler_registros():
        pontos = registro["pontos"]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = registro["nome"]
            data_jogada = f"{registro['data']} às {registro['hora']}"

    return nome_maior, maior_pontos, data_jogada
