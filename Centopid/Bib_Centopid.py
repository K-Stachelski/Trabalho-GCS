import pygame
from random import randint
import os

largura = 800
altura = 500

tela = pygame.display.set_mode((largura, altura))

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
        self.rect.x = randint(50, 700)
        self.rect.y = randint(50, 400)

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