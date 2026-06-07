import os
import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def caminho_asset(nome):
    return os.path.join(BASE_DIR, "assets", nome)

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load(caminho_asset("icone.png"))
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load(caminho_asset("background.jpg"))
largura_fundo = round(fundo.get_width() * tamanho[1] / fundo.get_height())
fundo = pygame.transform.scale(fundo, (largura_fundo, tamanho[1]))
fundoDead = pygame.image.load(caminho_asset("backgroundDead.jpg"))
fundoDead = pygame.transform.scale(fundoDead, tamanho)
fundoStart = pygame.image.load(caminho_asset("bv_sonic.png"))

iron = pygame.image.load(caminho_asset("IronMan.png"))
iron = pygame.transform.scale(iron, (116,51))
missel = pygame.image.load(caminho_asset("missile.png"))
missel = pygame.transform.scale(missel, (125,25))
pygame.mixer.music.load(caminho_asset("ironsound.mp3"))
fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    pygame.mixer.music.load(caminho_asset("ironsound.mp3"))
    topo_grama = 560
    limite_inferior_personagem = topo_grama - iron.get_height()
    fundoMov1 = 0
    fundoMov2 = largura_fundo
    posicaoXPersona = 0
    posicaoYPersona = limite_inferior_personagem
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    velocidadeMovPersona = 5
    posicaoXMissel = tamanho[0]
    posicaoYMissel = limite_inferior_personagem
    velocidadeMissel = 2
    pontos = 0
    pygame.mixer.music.play(-1)
    dificuldade = 20
    pausado = False
    pauseButton = pygame.Rect(10, 10, 120, 40)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
                movimentoXPersona = 0
            elif evento.type == pygame.MOUSEBUTTONUP and pauseButton.collidepoint(evento.pos):
                pausado = not pausado
                movimentoXPersona = 0
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                if not pausado:
                    movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                if not pausado:
                    movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                if not pausado:
                    movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                if not pausado:
                    movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        if pausado:
            pygame.draw.rect(tela, branco, pauseButton, border_radius=10)
            textoContinuar = fonteMenu.render("CONTINUAR", True, preto)
            textoContinuarRect = textoContinuar.get_rect(center=pauseButton.center)
            tela.blit(textoContinuar, textoContinuarRect)

            textoPausado = pygame.font.Font(None, 80).render("PAUSADO", True, branco)
            rectPausado = textoPausado.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2))
            tela.blit(textoPausado, rectPausado)
            pygame.display.update()
            relogio.tick(60)
            continue
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > tamanho[0] - iron.get_width():
            posicaoXPersona = tamanho[0] - iron.get_width()
        if posicaoYPersona < 450:
            posicaoYPersona = 450
        elif posicaoYPersona > limite_inferior_personagem:
            posicaoYPersona = limite_inferior_personagem
            
            
        posicaoXMissel = posicaoXMissel - velocidadeMissel
        if posicaoXMissel < -125:
            posicaoXMissel = tamanho[0]
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoYMissel = random.randint(450, topo_grama - missel.get_height())
                            
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )
        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -largura_fundo:
            fundoMov1 = largura_fundo
        elif fundoMov2 <= -largura_fundo:
            fundoMov2 = largura_fundo
        
        
        tela.blit(iron, (posicaoXPersona,posicaoYPersona))
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))

        pygame.draw.rect(tela, branco, pauseButton, border_radius=10)
        textoPause = fonteMenu.render("PAUSE", True, preto)
        textoPauseRect = textoPause.get_rect(center=pauseButton.center)
        tela.blit(textoPause, textoPauseRect)
            
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+51))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 125))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 25))
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho_asset("sonic_game_over.mp3"))
    pygame.mixer.music.play()
    larguraButtonStart = 220
    alturaButtonStart  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 220
                    alturaButtonStart  = 40

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 220
                    alturaButtonStart  = 40
                    jogar()
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (40,180, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        startTextoRect = startTexto.get_rect(center=startButton.center)
        tela.blit(startTexto, startTextoRect)


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 400
    alturaButtonStart  = 30

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 400
                    alturaButtonStart  = 30


            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 400
                    alturaButtonStart  = 30
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,300, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (170,300))

        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (50,50))


        pygame.display.update()
        relogio.tick(60)

start()
