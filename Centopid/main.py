import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os
import time
import Bib_Centopid

pygame.init()

# Reiniciar variáveis do jogo
def reiniciar():
    global pontos, tam_inicial, x_cobra, y_cobra, lista_cabeca, lista_cobra
    global velocidade, x_controle, y_controle, morreu, pausado
    pontos = 0
    tam_inicial = 2
    x_cobra = int(largura // 2)
    y_cobra = int(altura // 2)
    lista_cobra = []
    lista_cabeca = []
    velocidade = 2.5
    x_controle = velocidade
    y_controle = 0
    morreu = False
    pausado = False
    food.sortear_posicao()
# END REINICIAR

# Botoes
button_surface = pygame.image.load("imagens/play.png")
button_surface = pygame.transform.scale(button_surface, (210, 109))
button = Bib_Centopid.Button(button_surface, 363, 410)

button_surface2 = pygame.image.load("imagens/volta.png")
button_surface2 = pygame.transform.scale(button_surface2, (104, 79))
button2 = Bib_Centopid.Button(button_surface2, 52, 460)

button_sergio = pygame.image.load("imagens/sergio.png")
button_sergio = pygame.transform.scale(button_sergio, (205, 297))
sergio = Bib_Centopid.Button(button_sergio, 216, 237)

button_claudio = pygame.image.load("imagens/claudio.png")
button_claudio = pygame.transform.scale(button_claudio, (198, 293))
claudio = Bib_Centopid.Button(button_claudio, 493, 238)

button_curto = pygame.image.load("imagens/curto.png")
button_curto = pygame.transform.scale(button_curto, (183, 91))
curto = Bib_Centopid.Button(button_curto, 389, 222)

button_infinito = pygame.image.load("imagens/infinito.png")
button_infinito = pygame.transform.scale(button_infinito, (180, 91))
infinito = Bib_Centopid.Button(button_infinito, 394, 348)

button_surface3 = pygame.image.load("imagens/casa.png")
button_surface3 = pygame.transform.scale(button_surface3, (121, 122))
button3 = Bib_Centopid.Button(button_surface3, 81, 413)

# Comida
food = Bib_Centopid.Food(randint(120, 650), randint(120, 450))
grupo_sprites = pygame.sprite.Group()
grupo_sprites.add(food)

# Carregar imagens de fundo
BackGround = Bib_Centopid.Background('imagens/background.png', [0, 0])
Tela_Inicial = Bib_Centopid.Background('imagens/inicio.png', [0, 0])
Tela_Selecao = Bib_Centopid.Background('imagens/selecao.png', [0, 0])
Tela_Modo = Bib_Centopid.Background('imagens/modo.png', [0, 0])
Tela_Creditos = Bib_Centopid.Background('imagens/creditos.png', [0, 0])

# Tamanho da tela
largura = 800
altura = 500

# Inicializa variáveis locais
reiniciar()

fonte = pygame.font.SysFont('Comic Sans', 25, True, False)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('CENTOPID')
relogio = pygame.time.Clock()

cont = 0
rec0 = 0
rec, rec2 = Bib_Centopid.carregar_recordes()
inicio = 0
modo = 0
skin = 0
pausado = False

# Musica
pygame.mixer.init()
pygame.mixer.music.load('menu.mp3')
pygame.mixer.music.set_volume(0.3)        
pygame.mixer.music.play(-1)

while True:
    relogio.tick(60)

    # Tela de inicio
    if inicio == 0:
        tela.fill([255, 255, 255])
        tela.blit(Tela_Inicial.image, Tela_Inicial.rect)

        texto = f'Recorde: {rec0}'
        recorde = fonte.render(texto, True, (110, 75, 24))
        tela.blit(recorde, (295, 135))
        cont = 0
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    time.sleep(0.1)
                    inicio = 1
        button.update()

    # Tela de seleção de personagem 
    elif inicio == 1:
        tela.fill([255, 255, 255])
        tela.blit(Tela_Selecao.image, Tela_Selecao.rect)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if button2.rect.collidepoint(pygame.mouse.get_pos()):
                    time.sleep(0.1)
                    inicio = 0
                if sergio.rect.collidepoint(pygame.mouse.get_pos()):
                    skin = 0
                    time.sleep(0.1)
                    inicio = 2
                if claudio.rect.collidepoint(pygame.mouse.get_pos()):
                    skin = 1
                    time.sleep(0.1)
                    inicio = 2
                    
        button2.update()
        sergio.update()
        claudio.update()

    # Seleção do modo longo/infinito ou curto
    elif inicio == 2:
        tela.fill([255, 255, 255])
        tela.blit(Tela_Modo.image, Tela_Modo.rect)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if button2.rect.collidepoint(pygame.mouse.get_pos()):
                    time.sleep(0.1)
                    inicio = 1
                if curto.rect.collidepoint(pygame.mouse.get_pos()):
                    modo = 1
                    reiniciar()
                    time.sleep(0.3)
                    inicio = 3
                if infinito.rect.collidepoint(pygame.mouse.get_pos()):
                    modo = 2
                    reiniciar()
                    time.sleep(0.3)
                    inicio = 3
                    
        button2.update()
        curto.update()
        infinito.update()

    # Tela de gameplay do jogo
    elif inicio == 3:
        tela.fill([255, 255, 255])
        tela.blit(BackGround.image, BackGround.rect)
        grupo_sprites.draw(tela)

        if modo == 1:
            msg = f'Pontos: {pontos}/30'
        else:
            msg = f'Pontos: {pontos}'
            
        msg2 = f'Mortes: {cont}'

        if modo == 1:
            msg3 = f'Recorde: {rec}'
        else:
            msg3 = f'Recorde: {rec2}'

        textinho = fonte.render(msg, True, (161, 115, 66))
        textinho2 = fonte.render(msg2, True, (161, 115, 66))
        textinho3 = fonte.render(msg3, True, (161, 115, 66))

        tela.blit(textinho, (15, 5))
        tela.blit(textinho2, (15, 30))
        tela.blit(textinho3, (15, 55))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

            # Controle de movimento da centopeia
            if evento.type == KEYDOWN:
                if evento.key == K_p:
                    pausado = True
                elif (evento.key == K_a or evento.key == K_LEFT) and x_controle != velocidade:
                    x_controle = -velocidade
                    y_controle = 0
                elif (evento.key == K_d or evento.key == K_RIGHT) and x_controle != -velocidade:
                    x_controle = velocidade
                    y_controle = 0
                elif (evento.key == K_w or evento.key == K_UP) and y_controle != velocidade:
                    y_controle = -velocidade
                    x_controle = 0
                elif (evento.key == K_s or evento.key == K_DOWN) and y_controle != -velocidade:
                    y_controle = velocidade
                    x_controle = 0

        # Loop do estado de Jogo Pausado
        while pausado:
            fonte_pausa = pygame.font.SysFont('Comic Sans', 40, True, False)
            texto_pausa = fonte_pausa.render("JOGO PAUSADO", True, (255, 255, 255))
            texto_continuar = fonte.render("Pressione 'P' para continuar ou 'E' para sair", True, (255, 255, 255))
            
            ret_p = texto_pausa.get_rect(center=(400, 220))
            ret_c = texto_continuar.get_rect(center=(400, 270))

            s = pygame.Surface((largura, altura))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            tela.blit(s, (0, 0))
            
            tela.blit(texto_pausa, ret_p)
            tela.blit(texto_continuar, ret_c)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    exit()
                if evento.type == KEYDOWN:
                    if evento.key == K_p:
                        pausado = False
                    elif evento.key == K_e:
                        pausado = False
                        inicio = 0
                        rec0 = rec if modo == 1 else rec2
                        reiniciar()

        x_cobra += x_controle
        y_cobra += y_controle

        if skin == 0:
            cobrinha = pygame.draw.circle(tela, (44, 44, 44), (int(x_cobra), int(y_cobra)), 15)
        else:
            cobrinha = pygame.draw.circle(tela, (126, 20, 186), (int(x_cobra), int(y_cobra)), 15)

        # Paredes
        t_teto = pygame.draw.rect(tela, (0, 0, 0), (0, 0, 800, 1))
        t_chao = pygame.draw.rect(tela, (0, 0, 0), (0, 499, 800, 30))
        parede_esquerda = pygame.draw.rect(tela, (0, 0, 0), (0, 0, 2, 500))
        parede_direita = pygame.draw.rect(tela, (0, 0, 0), (799, 0, 30, 500))

        # Colisão com a comidinha
        if cobrinha.colliderect(food.rect):
            pontos += 1
            if modo == 1 and pontos >= rec:
                rec = pontos
                Bib_Centopid.salvar_recordes(rec, rec2)
            elif modo == 2 and pontos >= rec2:
                rec2 = pontos
                Bib_Centopid.salvar_recordes(rec, rec2)

            if not (modo == 1 and pontos >= 30):
                food.sortear_posicao()
                tam_inicial += 2
                velocidade += 0.2

        # Atualiza rastro da cobra
        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

        if len(lista_cobra) > tam_inicial:
            del lista_cobra[0]

        # Checa se a cabeça da centopeia colidiu com o corpo dela mesma
        auto_colisao = lista_cabeca in lista_cobra[:-1]

        # Checagem de Game Over
        if auto_colisao or cobrinha.colliderect(t_teto) or cobrinha.colliderect(t_chao) or cobrinha.colliderect(parede_direita) or cobrinha.colliderect(parede_esquerda):
            time.sleep(0.3)
            fonte2 = pygame.font.SysFont('Comic Sans', 25, True, False)
            fonte3 = pygame.font.SysFont('Comic Sans', 50, True, False)
            
            msg = 'GAME OVER'
            msg2 = "Pressione a tecla 'R' para reiniciar o jogo"
            msg3 = "ou pressione a tecla 'E' para voltar a tela inicial"
            
            textinho = fonte3.render(msg, True, (255, 255, 255))
            textinho2 = fonte2.render(msg2, True, (255, 255, 255))
            textinho3 = fonte3.render(msg3, True, (255, 255, 255))
            
            ret_textinho = textinho.get_rect(center=(400, 215))
            ret_textinho2 = textinho2.get_rect(center=(400, 250))
            ret_textinho3 = textinho3.get_rect(center=(400, 280))
            
            morreu = True

            while morreu:
                tela.fill((0, 0, 0))
                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        pygame.quit()
                        exit()

                    if evento.type == KEYDOWN:
                        if evento.key == K_r:
                            cont += 1
                            reiniciar()
                        if evento.key == K_e:
                            inicio = 0
                            rec0 = rec if modo == 1 else rec2
                            reiniciar()

                tela.blit(textinho, ret_textinho)
                tela.blit(textinho2, ret_textinho2)
                tela.blit(textinho3, ret_textinho3)
                pygame.display.flip()

        # Renderização do corpo da cobra
        if skin == 0:
            Bib_Centopid.aumenta_cobra(lista_cobra)
        else:
            Bib_Centopid.aumenta_cobra2(lista_cobra)

        # Tela de Vitória (Modo Curto)
        if modo == 1 and pontos >= 30:
            tela.fill([255, 255, 255])
            tela.blit(Tela_Creditos.image, Tela_Creditos.rect)
            while pontos >= 30:
                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        pygame.quit()
                        exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if button3.rect.collidepoint(pygame.mouse.get_pos()):
                            time.sleep(0.1)
                            inicio = 0
                            rec0 = rec
                            modo = 0
                            reiniciar()
                            break
                button3.update()
                pygame.display.flip()

    pygame.display.flip()