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
    try:
        banco = open(CAMINHO_BANCO, "r")
        banco.close()
    except FileNotFoundError:
        print("Banco de Dados Inexistente. Criando...")
        banco = open(CAMINHO_BANCO, "w")
        banco.close()
    
def escrever_dados(nome, pontos):
    banco = open(CAMINHO_BANCO, "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dicionario_dados = formato_json.loads(dados)
    else:
        dicionario_dados = {}
        
    data_hora_br = data_e_hora.now().strftime("%d/%m/%Y às %H:%M:%S")
    dicionario_dados[nome] = (pontos, data_hora_br)
    
    banco = open(CAMINHO_BANCO, "w")
    banco.write(formato_json.dumps(dicionario_dados))
    banco.close()
    
def maior_pontuador():
    banco = open(CAMINHO_BANCO, "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dicionario_dados = formato_json.loads(dados)
    else:
        dicionario_dados = {}

    nome_maior = None
    data_jogada = None
    maior_pontos = -1

    for nome, informacoes in dicionario_dados.items():
        pontos = informacoes[0]
        
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            data_jogada = informacoes[1]

    return nome_maior, maior_pontos, data_jogada
