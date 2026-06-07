import os, time
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BANCO = os.path.join(BASE_DIR, "base.atitus")

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open(CAMINHO_BANCO,"r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open(CAMINHO_BANCO,"w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open(CAMINHO_BANCO,"r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open(CAMINHO_BANCO,"w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo
    
def maior_pontuador():
    banco = open(CAMINHO_BANCO,"r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada =  None
    maior_pontos = -1

    for nome, info in dadosDict.items():

        pontos = info[0]
        
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            dataJogada = info[1]            

    return nome_maior, maior_pontos, dataJogada
