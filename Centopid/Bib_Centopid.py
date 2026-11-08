import pygame
import random
from random import randint
import os
import json
from config import (
    LARGURA_TELA,
    ALTURA_TELA,
    COR_SERGIO,
    COR_CLAUDIO,
    RAIO_CENTOPEIA,
)

largura = LARGURA_TELA
altura = ALTURA_TELA

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

        self.tipos = {
            "normal": {
                "pontos": 1,
                "crescimento": 2,
                "cor": (0, 255, 0)
            },
            "especial": {
                "pontos": 3,
                "crescimento": 4,
                "cor": (255, 255, 0)
            },
            "bonus": {
                "pontos": 5,
                "crescimento": 0,
                "cor": (180, 0, 255)
            }
        }

        self.imagem_original = pygame.image.load('imagens/comida.png').convert_alpha()

        self.rect = self.imagem_original.get_rect()
        self.rect.topleft = (x, y)

        self.sorteia_tipo()

    def sorteia_tipo(self):
        self.tipo = random.choices(
            ["normal", "especial", "bonus"],
            weights=[60, 25, 15],
            k=1
        )[0]

        dados = self.tipos[self.tipo]
        self.pontos = dados["pontos"]
        self.crescimento = dados["crescimento"]

        self.image = self.imagem_original.copy()
        self.image.fill(dados["cor"], special_flags=pygame.BLEND_RGBA_MULT)

    def sortear_posicao(self):
        self.rect.x = randint(0, largura - self.rect.width)
        self.rect.y = randint(0, altura - self.rect.height)
        self.sorteia_tipo()

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
        pygame.draw.circle(tela, COR_SERGIO, (int(xy[0]), int(xy[1])), RAIO_CENTOPEIA) # skin Sérgio

def aumenta_cobra2(lista_cobra):
    for xy in lista_cobra:
        pygame.draw.circle(tela, COR_CLAUDIO, (int(xy[0]), int(xy[1])), RAIO_CENTOPEIA) # skin Cláudio
class ComidaEspecial(pygame.sprite.Sprite):
    """Representa uma comida dourada que bonifica com mais pontos."""
    def __init__(self, largura_limite=800, altura_limite=500):
        super().__init__()
        self.largura_limite = largura_limite
        self.altura_limite = altura_limite
        self.tamanho = 18
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        # Comida dourada/amarela brilhante
        pygame.draw.circle(self.image, (255, 215, 0), (self.tamanho // 2, self.tamanho // 2), self.tamanho // 2)
        pygame.draw.circle(self.image, (255, 255, 255), (self.tamanho // 2 - 2, self.tamanho // 2 - 2), 3)
        self.rect = self.image.get_rect()
        self.ativa = False
        self.sortear_posicao()

    def sortear_posicao(self):
        # 30% de chance de aparecer a cada rodada
        if randint(1, 10) <= 3:
            self.rect.x = randint(80, self.largura_limite - 80)
            self.rect.y = randint(80, self.altura_limite - 80)
            self.ativa = True
        else:
            self.ativa = False
            self.rect.x = -100
            self.rect.y = -100

class Inimigo(pygame.sprite.Sprite):
    """Representa um obstaculo inimigo estatico ou movel que causa game over."""
    def __init__(self, largura_limite=800, altura_limite=500):
        super().__init__()
        self.largura_limite = largura_limite
        self.altura_limite = altura_limite
        self.tamanho = 22
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        # Inimigo com formato e tom avermelhado de alerta
        pygame.draw.circle(self.image, (220, 20, 60), (self.tamanho // 2, self.tamanho // 2), self.tamanho // 2)
        pygame.draw.circle(self.image, (0, 0, 0), (self.tamanho // 2, self.tamanho // 2), self.tamanho // 4)
        self.rect = self.image.get_rect()
        self.ativo = False
        self.sortear_posicao()

    def sortear_posicao(self):
        # Surge a partir de 5 pontos
        self.rect.x = randint(100, self.largura_limite - 100)
        self.rect.y = randint(100, self.altura_limite - 100)
        self.ativo = True