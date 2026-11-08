import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os
import time
import Bib_Centopid
from config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    COR_BRANCO,
    COR_PRETO,
    COR_SERGIO,
    COR_CLAUDIO,
    COR_TEXTO_MENU,
    COR_TEXTO_HUD,
    VELOCIDADE_INICIAL,
    INCREMENTO_VELOCIDADE,
    TAMANHO_INICIAL,
    INCREMENTO_TAMANHO,
    RAIO_CENTOPEIA,
    PONTUACAO_VITORIA_MODO_CURTO,
)

# Garante que o diretorio de execucao seja a pasta onde os recursos do jogo estao localizados
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Mapeamento de direcoes opostas para prevencao de auto-colisao imediata (Issue #26)
DIRECOES_OPOSTAS = {
    'ESQUERDA': 'DIREITA',
    'DIREITA': 'ESQUERDA',
    'CIMA': 'BAIXO',
    'BAIXO': 'CIMA',
}

# Reiniciar variáveis do jogo (incluindo o estado de pausa)
def reiniciar():
    global pontos, tam_inicial, x_cobra, y_cobra, lista_cabeca, lista_cobra
    global velocidade, x_controle, y_controle, morreu, pausado, direcao_atual, proxima_direcao
    pontos = 0
    tam_inicial = TAMANHO_INICIAL
    x_cobra = int(LARGURA_TELA // 2)
    y_cobra = int(ALTURA_TELA // 2)
    lista_cobra = []
    lista_cabeca = []
    velocidade = VELOCIDADE_INICIAL
    x_controle = velocidade
    y_controle = 0
    direcao_atual = 'DIREITA'
    proxima_direcao = 'DIREITA'
    morreu = False
    pausado = False
    food.sortear_posicao()
    comida_especial.sortear_posicao()
    inimigo.sortear_posicao()
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

# Carregar imagens de fundo
BackGround = Bib_Centopid.Background('imagens/background.png', [0, 0])
Tela_Inicial = Bib_Centopid.Background('imagens/inicio.png', [0, 0])
Tela_Selecao = Bib_Centopid.Background('imagens/selecao.png', [0, 0])
Tela_Modo = Bib_Centopid.Background('imagens/modo.png', [0, 0])
Tela_Creditos = Bib_Centopid.Background('imagens/creditos.png', [0, 0])

# Tamanho da tela
largura = LARGURA_TELA
altura = ALTURA_TELA

# Comida e Elementos Dinamicos
food = Bib_Centopid.Food(randint(120, 650), randint(120, 450))
comida_especial = Bib_Centopid.ComidaEspecial(largura, altura)
inimigo = Bib_Centopid.Inimigo(largura, altura)

grupo_sprites = pygame.sprite.Group()
grupo_sprites.add(food)

# Inicializa variáveis locais
reiniciar()

fonte = pygame.font.SysFont('Comic Sans', 25, True, False)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('CENTOPID')
relogio = pygame.time.Clock()

cont = 0
recordes = Bib_Centopid.carregar_recordes()
rec0 = recordes['rec0']
rec = recordes['rec']
rec2 = recordes['rec2']
inicio = 0
modo = 0
skin = 0

while True:
    relogio.tick(FPS)

    # Tela de inicio
    if inicio == 0:
        tela.fill(COR_BRANCO)
        tela.blit(Tela_Inicial.image, Tela_Inicial.rect)

        texto = f'Recorde: {rec0}'
        recorde = fonte.render(texto, True, COR_TEXTO_MENU)
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
        tela.fill(COR_BRANCO)
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
        tela.fill(COR_BRANCO)
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
        tela.fill(COR_BRANCO)
        tela.blit(BackGround.image, BackGround.rect)
        grupo_sprites.draw(tela)

        # Desenha os novos elementos (Issues #2 e #3)
        if comida_especial.ativa:
            tela.blit(comida_especial.image, comida_especial.rect)
        if inimigo.ativo:
            tela.blit(inimigo.image, inimigo.rect)

        if modo == 1:
            msg = f'Pontos: {pontos}/{PONTUACAO_VITORIA_MODO_CURTO}'
        else:
            msg = f'Pontos: {pontos}'
            
        msg2 = f'Mortes: {cont}'

        if modo == 1:
            msg3 = f'Recorde: {rec}'
        else:
            msg3 = f'Recorde: {rec2}'

        msg_modo = f'Modo: {"Curto" if modo == 1 else "Infinito"}'
        msg_fps = f'FPS: {FPS}'

        textinho = fonte.render(msg, True, COR_TEXTO_HUD)
        textinho2 = fonte.render(msg2, True, COR_TEXTO_HUD)
        textinho3 = fonte.render(msg3, True, COR_TEXTO_HUD)
        textinho_modo = fonte.render(msg_modo, True, COR_TEXTO_HUD)
        textinho_fps = fonte.render(msg_fps, True, COR_TEXTO_HUD)

        tela.blit(textinho, (15, 5))
        tela.blit(textinho2, (15, 30))
        tela.blit(textinho3, (15, 55))
        tela.blit(textinho_modo, (15, 80))
        tela.blit(textinho_fps, (15, 105))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

            if evento.type == KEYDOWN:
                # Tecla P para pausar/despausar o jogo
                if evento.key == K_p:
                    pausado = not pausado

                # Controle de movimento da centopeia (só processa se não estiver pausado)
                if not pausado:
                    nova_dir = None
                    if evento.key == K_a or evento.key == K_LEFT:
                        nova_dir = 'ESQUERDA'
                    elif evento.key == K_d or evento.key == K_RIGHT:
                        nova_dir = 'DIREITA'
                    elif evento.key == K_w or evento.key == K_UP:
                        nova_dir = 'CIMA'
                    elif evento.key == K_s or evento.key == K_DOWN:
                        nova_dir = 'BAIXO'

                    if nova_dir is not None:
                        if DIRECOES_OPOSTAS.get(nova_dir) != direcao_atual and DIRECOES_OPOSTAS.get(nova_dir) != proxima_direcao:
                            proxima_direcao = nova_dir

        # Se o jogo estiver pausado, exibe a mensagem de pausa e congela as atualizações lógicas
        if pausado:
            msg_pausa = fonte.render("JOGO PAUSADO - Pressione 'P' para continuar", True, COR_PRETO)
            ret_pausa = msg_pausa.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(msg_pausa, ret_pausa)
            pygame.display.flip()
            continue

        direcao_atual = proxima_direcao
        if direcao_atual == 'ESQUERDA':
            x_controle = -velocidade
            y_controle = 0
        elif direcao_atual == 'DIREITA':
            x_controle = velocidade
            y_controle = 0
        elif direcao_atual == 'CIMA':
            x_controle = 0
            y_controle = -velocidade
        elif direcao_atual == 'BAIXO':
            x_controle = 0
            y_controle = velocidade

        x_cobra += x_controle
        y_cobra += y_controle

        if skin == 0:
            cobrinha = pygame.draw.circle(tela, COR_SERGIO, (int(x_cobra), int(y_cobra)), RAIO_CENTOPEIA)
        else:
            cobrinha = pygame.draw.circle(tela, COR_CLAUDIO, (int(x_cobra), int(y_cobra)), RAIO_CENTOPEIA)

        # Paredes
        t_teto = pygame.draw.rect(tela, COR_PRETO, (0, 0, LARGURA_TELA, 1))
        t_chao = pygame.draw.rect(tela, COR_PRETO, (0, ALTURA_TELA - 1, LARGURA_TELA, 30))
        parede_esquerda = pygame.draw.rect(tela, COR_PRETO, (0, 0, 2, ALTURA_TELA))
        parede_direita = pygame.draw.rect(tela, COR_PRETO, (LARGURA_TELA - 1, 0, 30, ALTURA_TELA))

        # Colisão com a comidinha padrão
        if cobrinha.colliderect(food.rect):
            pontos += 1
            novo_recorde = False
            if modo == 1 and pontos > rec:
                rec = pontos
                rec0 = max(rec0, rec)
                novo_recorde = True
            elif modo == 2 and pontos > rec2:
                rec2 = pontos
                rec0 = max(rec0, rec2)
                novo_recorde = True

            if novo_recorde:
                Bib_Centopid.salvar_recordes({'rec0': rec0, 'rec': rec, 'rec2': rec2})

            if not (modo == 1 and pontos >= PONTUACAO_VITORIA_MODO_CURTO):
                food.sortear_posicao()
                tam_inicial += INCREMENTO_TAMANHO
                velocidade += INCREMENTO_VELOCIDADE

        # Colisão com a comida especial (Issue #3)
        if comida_especial.ativa and cobrinha.colliderect(comida_especial.rect):
            pontos += 3
            novo_recorde = False
            if modo == 1 and pontos > rec:
                rec = pontos
                rec0 = max(rec0, rec)
                novo_recorde = True
            elif modo == 2 and pontos > rec2:
                rec2 = pontos
                rec0 = max(rec0, rec2)
                novo_recorde = True

            if novo_recorde:
                Bib_Centopid.salvar_recordes({'rec0': rec0, 'rec': rec, 'rec2': rec2})

            comida_especial.sortear_posicao()
            inimigo.sortear_posicao()
            tam_inicial += 3

        # Atualiza rastro da cobra
        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

        if len(lista_cobra) > tam_inicial:
            del lista_cobra[0]

        # Checa se a cabeça da centopeia colidiu com o corpo dela mesma
        auto_colisao = lista_cabeca in lista_cobra[:-1]

        # Checa colisão com o inimigo (Issue #2)
        colisao_inimigo = inimigo.ativo and cobrinha.colliderect(inimigo.rect)

        # Checagem de Game Over
        if auto_colisao or colisao_inimigo or cobrinha.colliderect(t_teto) or cobrinha.colliderect(t_chao) or cobrinha.colliderect(parede_direita) or cobrinha.colliderect(parede_esquerda):
            time.sleep(0.3)
            fonte2 = pygame.font.SysFont('Comic Sans', 25, True, False)
            fonte3 = pygame.font.SysFont('Comic Sans', 50, True, False)
            
            msg = 'GAME OVER'
            msg2 = "Pressione a tecla 'R' para reiniciar o jogo"
            msg3 = "ou pressione a tecla 'E' para voltar a tela inicial"
            
            textinho = fonte3.render(msg, True, COR_BRANCO)
            textinho2 = fonte2.render(msg2, True, COR_BRANCO)
            textinho3 = fonte2.render(msg3, True, COR_BRANCO)
            
            ret_textinho = textinho.get_rect(center=(400, 215))
            ret_textinho2 = textinho2.get_rect(center=(400, 250))
            ret_textinho3 = textinho3.get_rect(center=(400, 280))
            
            morreu = True

            while morreu:
                tela.fill(COR_PRETO)
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
                            Bib_Centopid.salvar_recordes({'rec0': rec0, 'rec': rec, 'rec2': rec2})
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
        if modo == 1 and pontos >= PONTUACAO_VITORIA_MODO_CURTO:
            tela.fill(COR_BRANCO)
            tela.blit(Tela_Creditos.image, Tela_Creditos.rect)
            while pontos >= PONTUACAO_VITORIA_MODO_CURTO:
                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        pygame.quit()
                        exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if button3.rect.collidepoint(pygame.mouse.get_pos()):
                            time.sleep(0.1)
                            inicio = 0
                            rec0 = rec
                            Bib_Centopid.salvar_recordes({'rec0': rec0, 'rec': rec, 'rec2': rec2})
                            modo = 0
                            reiniciar()
                            break
                button3.update()
                pygame.display.flip()

    pygame.display.flip()