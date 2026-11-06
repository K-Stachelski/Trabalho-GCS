import pygame
from random import randint

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