import os

import pygame


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ASSETS = os.path.join(BASE_DIR, "assets")


def caminho_asset(nome):
    return os.path.join(PASTA_ASSETS, nome)


def carregar_imagem(nome, tamanho=None):
    imagem = pygame.image.load(caminho_asset(nome))
    if tamanho is not None:
        imagem = pygame.transform.scale(imagem, tamanho)
    return imagem


def carregar_musica(nome):
    pygame.mixer.music.load(caminho_asset(nome))
