import pygame
from random import randint
import os
import json

largura = 800
altura = 500

tela = pygame.display.set_mode((largura, altura))

CAMINHO_PADRAO_RECORDES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordes.json')
RECORDES_PADRAO = {'rec0': 0, 'rec': 0, 'rec2': 0}

def salvar_recordes(recordes, caminho=None):
    if caminho is None:
        caminho = CAMINHO_PADRAO_RECORDES

    dados_salvar = {}
    for chave in ('rec0', 'rec', 'rec2'):
        try:
            val = int(recordes.get(chave, 0))
            dados_salvar[chave] = max(0, val)
        except (ValueError, TypeError):
            dados_salvar[chave] = 0

    try:
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_salvar, f, indent=4)
        return True
    except OSError:
        return False

def carregar_recordes(caminho=None):
    if caminho is None:
        caminho = CAMINHO_PADRAO_RECORDES

    if not os.path.exists(caminho):
        salvar_recordes(RECORDES_PADRAO, caminho)
        return dict(RECORDES_PADRAO)

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        if not isinstance(dados, dict):
            raise ValueError("Conteúdo de recordes não é um dicionário")

        recordes_validos = {}
        for chave in ('rec0', 'rec', 'rec2'):
            valor = dados.get(chave)
            if isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0:
                recordes_validos[chave] = valor
            else:
                raise ValueError(f"Valor inválido ou ausente para a chave: {chave}")

        return recordes_validos
    except Exception:
        salvar_recordes(RECORDES_PADRAO, caminho)
        return dict(RECORDES_PADRAO)

# Carregar Fundo de tela
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__() 
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# Sprite Comidinha
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('imagens/comida.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def sortear_posicao(self):
        self.rect.x = randint(0, largura - self.rect.width)
        self.rect.y = randint(0, altura - self.rect.height)

# Cria botoes
class Button():
    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        tela.blit(self.image, self.rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            print("Button Press!")

def carregar_arquivos():
    diretorio = os.path.join(os.getcwd(), 'Centopid/imagens')
    return diretorio

def aumenta_cobra(lista_cobra):
    for xy in lista_cobra:
        pygame.draw.circle(tela, (44, 44, 44), (int(xy[0]), int(xy[1])), 15) # skin Sérgio

def aumenta_cobra2(lista_cobra):
    for xy in lista_cobra:
        pygame.draw.circle(tela, (126, 20, 186), (int(xy[0]), int(xy[1])), 15) # skin Cláudio