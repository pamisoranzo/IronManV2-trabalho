import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import carregar_imagem, carregar_musica

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
icone = carregar_imagem("icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = carregar_imagem("background.jpg")
largura_fundo = round(fundo.get_width() * tamanho[1] / fundo.get_height())
fundo = pygame.transform.scale(fundo, (largura_fundo, tamanho[1]))
fundoDead = carregar_imagem("backgroundDead.jpg", tamanho)
fundoStart = carregar_imagem("bv_sonic.png")

iron = carregar_imagem("IronMan.png", (116,51))
missel = carregar_imagem("missile.png", (125,25))
carregar_musica("ironsound.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteTitulo = pygame.font.SysFont("comicsans",24, bold=True)
fonteTexto = pygame.font.SysFont("comicsans",17)
fonteInstrucao = pygame.font.SysFont("comicsans",15)

def jogar():
    carregar_musica("ironsound.mp3")
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
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                movimentoXPersona = 0
                movimentoYPersona = 0
                if pausado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif evento.type == pygame.MOUSEBUTTONUP and pauseButton.collidepoint(evento.pos):
                pausado = not pausado
                movimentoXPersona = 0
                movimentoYPersona = 0
                if pausado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
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

            textoPausado = pygame.font.Font(None, 80).render("PAUSE", True, branco)
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

        instrucaoPause = fonteMenu.render("Press Space to Pause Game.", True, branco)
        tela.blit(instrucaoPause, (10, 60))
            
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
    carregar_musica("sonic_game_over.mp3")
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
    alturaButtonStart  = 50

    if nome_maior is None:
        texto_recorde = "Ainda não há recorde registrado."
    else:
        texto_recorde = (
            f"Recorde: {nome_maior} - {maior_pontos} pontos - {dataJogada}"
        )

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 400
                    alturaButtonStart  = 50


            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 400
                    alturaButtonStart  = 50
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))

        titulo = fonteTitulo.render(f"Bem-vindo(a), {nome}!", True, branco)
        tela.blit(titulo, (40, 35))

        subtitulo = fonteTexto.render("Como jogar:", True, branco)
        tela.blit(subtitulo, (40, 85))

        instrucoes = [
            "Use as setas do teclado para movimentar o personagem.",
            "Desvie dos mísseis e tente alcançar a maior pontuação.",
            "Durante a partida, pressione Espaço para pausar ou continuar.",
        ]
        for indice, instrucao in enumerate(instrucoes):
            texto_instrucao = fonteInstrucao.render(instrucao, True, branco)
            tela.blit(texto_instrucao, (55, 120 + indice * 32))

        recorde = fonteTexto.render(texto_recorde, True, branco)
        tela.blit(recorde, (40, 235))

        startButton = pygame.draw.rect(
            tela,
            branco,
            (300, 560, larguraButtonStart, alturaButtonStart),
            border_radius=15,
        )
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        startTextoRect = startTexto.get_rect(center=startButton.center)
        tela.blit(startTexto, startTextoRect)

        pygame.display.update()
        relogio.tick(60)

start()
