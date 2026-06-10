import os as sistema_operacional
import sys as sistema

import pygame


DIRETORIO_BASE = (
    sistema_operacional.path.dirname(sistema.executable)
    if getattr(sistema, "frozen", False)
    else sistema_operacional.path.dirname(
        sistema_operacional.path.dirname(
            sistema_operacional.path.abspath(__file__)
        )
    )
)
PASTA_RECURSOS = sistema_operacional.path.join(DIRETORIO_BASE, "bases")


def caminho_recurso(nome):
    return sistema_operacional.path.join(PASTA_RECURSOS, nome)


def carregar_imagem(nome, tamanho=None):
    imagem = pygame.image.load(caminho_recurso(nome))
    if tamanho is not None:
        imagem = pygame.transform.scale(imagem, tamanho)
    return imagem


def carregar_musica(nome):
    pygame.mixer.music.load(caminho_recurso(nome))
