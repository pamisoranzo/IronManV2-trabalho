import math as matematica
import pygame
import random as aleatorio
from recursos.funcoes import (
    escrever_dados,
    inicializar_banco_de_dados,
    limpar_tela,
    maior_pontuador,
)
from recursos.trabalho import carregar_imagem, carregar_musica

limpar_tela()
inicializar_banco_de_dados()
nome_maior, maior_pontos, data_jogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Sonic do Marcão")
icone = carregar_imagem("icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = carregar_imagem("fundo_jogo.jpg")
largura_fundo = round(fundo.get_width() * tamanho[1] / fundo.get_height())
fundo = pygame.transform.scale(fundo, (largura_fundo, tamanho[1]))
fundo_derrota = carregar_imagem("fundo_derrota.jpg", tamanho)
fundo_inicio = carregar_imagem("tela_boas_vindas.png")

sonic_voando = carregar_imagem("sonic_voando.png", (90,56))
quadros_sonic_bola = [
    carregar_imagem(f"sonic_bola_{indice}.png", (50,50)) for indice in range(6)
]
bola_de_fogo = carregar_imagem("bola_de_fogo.png", (100, 51))
vilao_decorativo = carregar_imagem("vilao_decorativo.png", (90,99))
sol_decorativo = carregar_imagem("sol_decorativo.png")
carregar_musica("musica_partida.mp3")
fonte_menu = pygame.font.SysFont("comicsans",18)
fonte_titulo = pygame.font.SysFont("comicsans",24, bold=True)
fonte_texto = pygame.font.SysFont("comicsans",17)
fonte_instrucao = pygame.font.SysFont("comicsans",15)

def fechar_jogo():
    pygame.quit()
    raise SystemExit

def jogar():
    carregar_musica("musica_partida.mp3")
    topo_grama = 560
    limite_superior_personagem = 360
    posicao_inicial_personagem = 60
    posicao_fundo_1 = 0
    posicao_fundo_2 = largura_fundo
    posicao_x_personagem = posicao_inicial_personagem
    posicao_y_personagem = topo_grama - sonic_voando.get_height()
    movimento_x_personagem = 0
    movimento_y_personagem = 0
    velocidade_personagem = 5
    em_bola = False
    quadro_bola = 0
    contador_animacao_bola = 0
    posicao_x_bola_de_fogo = tamanho[0]
    posicao_y_bola_de_fogo = aleatorio.randint(
        390, topo_grama - bola_de_fogo.get_height()
    )
    velocidade_bola_de_fogo = 2
    posicao_x_decorativo = aleatorio.randint(
        300, tamanho[0] - vilao_decorativo.get_width()
    )
    posicao_y_decorativo = aleatorio.randint(80, 300)
    velocidade_x_decorativo = aleatorio.choice((-1, 1)) * aleatorio.uniform(0.6, 1.4)
    velocidade_y_decorativo = aleatorio.choice((-1, 1)) * aleatorio.uniform(0.4, 1.0)
    pontos = 0
    pygame.mixer.music.play(-1)
    dificuldade = 20
    pausado = False
    botao_pausa = pygame.Rect(10, 10, 120, 40)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fechar_jogo()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                movimento_x_personagem = 0
                movimento_y_personagem = 0
                if pausado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif evento.type == pygame.MOUSEBUTTONUP and botao_pausa.collidepoint(evento.pos):
                pausado = not pausado
                movimento_x_personagem = 0
                movimento_y_personagem = 0
                if pausado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                if not pausado:
                    movimento_y_personagem = -velocidade_personagem
                    em_bola = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                if not pausado:
                    movimento_y_personagem = velocidade_personagem
                    em_bola = True
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimento_y_personagem = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimento_y_personagem = 0
                em_bola = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimento_x_personagem = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimento_x_personagem = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimento_x_personagem = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimento_x_personagem = 0

        if pausado:
            pygame.draw.rect(tela, branco, botao_pausa, border_radius=10)
            texto_continuar = fonte_menu.render("CONTINUAR", True, preto)
            retangulo_texto_continuar = texto_continuar.get_rect(center=botao_pausa.center)
            tela.blit(texto_continuar, retangulo_texto_continuar)

            texto_pausado = pygame.font.Font(None, 80).render("PAUSADO", True, branco)
            retangulo_pausado = texto_pausado.get_rect(
                center=(tamanho[0] // 2, tamanho[1] // 2)
            )
            tela.blit(texto_pausado, retangulo_pausado)
            pygame.display.update()
            relogio.tick(60)
            continue
        
        posicao_x_personagem += movimento_x_personagem
        posicao_y_personagem += movimento_y_personagem
        personagem_atual = quadros_sonic_bola[quadro_bola] if em_bola else sonic_voando
        limite_inferior_personagem = topo_grama - personagem_atual.get_height()
        if posicao_x_personagem < posicao_inicial_personagem:
            posicao_x_personagem = posicao_inicial_personagem
        elif posicao_x_personagem > tamanho[0] - sonic_voando.get_width():
            posicao_x_personagem = tamanho[0] - sonic_voando.get_width()
        if posicao_y_personagem < limite_superior_personagem:
            posicao_y_personagem = limite_superior_personagem
        elif posicao_y_personagem > limite_inferior_personagem:
            posicao_y_personagem = limite_inferior_personagem
            
            
        posicao_x_bola_de_fogo -= velocidade_bola_de_fogo
        if posicao_x_bola_de_fogo < -bola_de_fogo.get_width():
            posicao_x_bola_de_fogo = tamanho[0]
            pontos = pontos + 1
            velocidade_bola_de_fogo += 1
            posicao_y_bola_de_fogo = aleatorio.randint(
                390, topo_grama - bola_de_fogo.get_height()
            )

        posicao_x_decorativo += velocidade_x_decorativo
        posicao_y_decorativo += velocidade_y_decorativo
        limite_x_decorativo = tamanho[0] - vilao_decorativo.get_width()
        limite_y_decorativo = topo_grama - vilao_decorativo.get_height()
        if posicao_x_decorativo <= 0 or posicao_x_decorativo >= limite_x_decorativo:
            posicao_x_decorativo = max(
                0, min(posicao_x_decorativo, limite_x_decorativo)
            )
            velocidade_x_decorativo = -velocidade_x_decorativo
            velocidade_y_decorativo = (
                aleatorio.choice((-1, 1)) * aleatorio.uniform(0.4, 1.0)
            )
        if posicao_y_decorativo <= 70 or posicao_y_decorativo >= limite_y_decorativo:
            posicao_y_decorativo = max(
                70, min(posicao_y_decorativo, limite_y_decorativo)
            )
            velocidade_y_decorativo = -velocidade_y_decorativo
            velocidade_x_decorativo = (
                aleatorio.choice((-1, 1)) * aleatorio.uniform(0.6, 1.4)
            )
                            
        tela.fill(branco)
        tela.blit(fundo, (posicao_fundo_1, 0))
        tela.blit(fundo, (posicao_fundo_2, 0))

        tempo_pulso = pygame.time.get_ticks() / 1000
        escala_pulso = 1 + 0.1 * matematica.sin(tempo_pulso * 2)
        largura_sol = round(sol_decorativo.get_width() * escala_pulso)
        altura_sol = round(sol_decorativo.get_height() * escala_pulso)
        sol_pulsando = pygame.transform.smoothscale(
            sol_decorativo, (largura_sol, altura_sol)
        )
        posicao_sol = (tamanho[0] - largura_sol, 0)
        tela.blit(sol_pulsando, posicao_sol)

        posicao_fundo_1 -= 1
        posicao_fundo_2 -= 1
        if posicao_fundo_1 <= -largura_fundo:
            posicao_fundo_1 = largura_fundo
        elif posicao_fundo_2 <= -largura_fundo:
            posicao_fundo_2 = largura_fundo
        
        
        if em_bola:
            personagem_atual = quadros_sonic_bola[quadro_bola]
            contador_animacao_bola += 1
            if contador_animacao_bola >= 5:
                contador_animacao_bola = 0
                quadro_bola = (quadro_bola + 1) % len(quadros_sonic_bola)

        tela.blit(vilao_decorativo, (posicao_x_decorativo, posicao_y_decorativo))
        tela.blit(personagem_atual, (posicao_x_personagem, posicao_y_personagem))
        tela.blit(
            bola_de_fogo,
            (posicao_x_bola_de_fogo, posicao_y_bola_de_fogo),
        )
        texto = fonte_menu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (700,15))

        pygame.draw.rect(tela, branco, botao_pausa, border_radius=10)
        texto_pausa = fonte_menu.render("PAUSAR", True, preto)
        retangulo_texto_pausa = texto_pausa.get_rect(center=botao_pausa.center)
        tela.blit(texto_pausa, retangulo_texto_pausa)

        instrucao_pausa = fonte_menu.render(
            "Pressione Espaço para pausar o jogo.", True, branco
        )
        tela.blit(instrucao_pausa, (10, 60))
            
        pixels_personagem_x = list(
            range(
                posicao_x_personagem,
                posicao_x_personagem + personagem_atual.get_width(),
            )
        )
        pixels_personagem_y = list(
            range(
                posicao_y_personagem,
                posicao_y_personagem + personagem_atual.get_height(),
            )
        )
        pixels_bola_de_fogo_x = list(
            range(
                posicao_x_bola_de_fogo,
                posicao_x_bola_de_fogo + bola_de_fogo.get_width(),
            )
        )
        pixels_bola_de_fogo_y = list(
            range(
                posicao_y_bola_de_fogo,
                posicao_y_bola_de_fogo + bola_de_fogo.get_height(),
            )
        )
        if (
            len(set(pixels_bola_de_fogo_y).intersection(pixels_personagem_y))
            > dificuldade
        ):
            if (
                len(set(pixels_bola_de_fogo_x).intersection(pixels_personagem_x))
                > dificuldade
            ):
                escrever_dados(nome, pontos)
                tela_derrota()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        
        pygame.display.update()
        relogio.tick(60)

def tela_derrota():
    pygame.mixer.music.stop()
    carregar_musica("musica_fim_de_jogo.mp3")
    pygame.mixer.music.play()
    nome_recordista, pontos_recordista, data_recorde = maior_pontuador()
    if nome_recordista is None:
        texto_recordista = "Ainda não há recorde registrado."
    else:
        texto_recordista = (
            f"Maior competidor: {nome_recordista} - "
            f"{pontos_recordista} pontos - {data_recorde}"
        )
    largura_botao_iniciar = 220
    altura_botao_iniciar = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fechar_jogo()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    largura_botao_iniciar = 220
                    altura_botao_iniciar = 40

            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if botao_iniciar.collidepoint(evento.pos):
                    largura_botao_iniciar = 220
                    altura_botao_iniciar = 40
                    jogar()
            
        tela.fill(branco)
        tela.blit(fundo_derrota, (0, 0))
        botao_iniciar = pygame.draw.rect(
            tela,
            branco,
            (40, 180, largura_botao_iniciar, altura_botao_iniciar),
            border_radius=15,
        )
        texto_iniciar = fonte_menu.render("Iniciar jogo", True, preto)
        retangulo_texto_iniciar = texto_iniciar.get_rect(center=botao_iniciar.center)
        tela.blit(texto_iniciar, retangulo_texto_iniciar)

        recordista = fonte_texto.render(texto_recordista, True, branco)
        tela.blit(recordista, (40, 240))

        pygame.display.update()
        relogio.tick(60)



def tela_inicio():
    largura_botao_iniciar = 400
    altura_botao_iniciar = 50

    if nome_maior is None:
        texto_recorde = "Ainda não há recorde registrado."
    else:
        texto_recorde = (
            f"Recorde: {nome_maior} - {maior_pontos} pontos - {data_jogada}"
        )

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fechar_jogo()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    largura_botao_iniciar = 400
                    altura_botao_iniciar = 50

            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if botao_iniciar.collidepoint(evento.pos):
                    largura_botao_iniciar = 400
                    altura_botao_iniciar = 50
                    jogar()

        tela.fill(branco)
        tela.blit(fundo_inicio, (0, 0))

        titulo = fonte_titulo.render(f"Bem-vindo(a), {nome}!", True, branco)
        tela.blit(titulo, (40, 35))

        subtitulo = fonte_texto.render("Como jogar:", True, branco)
        tela.blit(subtitulo, (40, 85))

        instrucoes = [
            "Use as setas do teclado para movimentar o personagem.",
            "Desvie das bolas de fogo e tente alcançar a maior pontuação.",
            "Durante a partida, pressione Espaço para pausar ou continuar.",
        ]
        for indice, instrucao in enumerate(instrucoes):
            texto_instrucao = fonte_instrucao.render(instrucao, True, branco)
            tela.blit(texto_instrucao, (55, 120 + indice * 32))

        recorde = fonte_texto.render(texto_recorde, True, branco)
        tela.blit(recorde, (40, 235))

        botao_iniciar = pygame.draw.rect(
            tela,
            branco,
            (300, 560, largura_botao_iniciar, altura_botao_iniciar),
            border_radius=15,
        )
        texto_iniciar = fonte_menu.render("Iniciar jogo", True, preto)
        retangulo_texto_iniciar = texto_iniciar.get_rect(center=botao_iniciar.center)
        tela.blit(texto_iniciar, retangulo_texto_iniciar)

        pygame.display.update()
        relogio.tick(60)

tela_inicio()
