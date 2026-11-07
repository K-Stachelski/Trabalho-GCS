"""
Testes unitários automatizados para o jogo Centopid.
Valida o módulo de configuração (Issue #30) e a lógica de prevenção de auto-colisão (Issue #26).
"""

import unittest
import os
import sys

# Garante suporte a execucao em ambientes headless (CI/CD / terminal)
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

# Adiciona o diretorio Centopid ao sys.path para importacao
CENTOPID_DIR = os.path.dirname(os.path.abspath(__file__))
if CENTOPID_DIR not in sys.path:
    sys.path.insert(0, CENTOPID_DIR)
os.chdir(CENTOPID_DIR)

import config
import Bib_Centopid


class TestConfiguracao(unittest.TestCase):
    """Testes para validar o modulo de configuracao (Issue #30)."""

    def test_constantes_dimensoes(self):
        self.assertEqual(config.LARGURA_TELA, 800)
        self.assertEqual(config.ALTURA_TELA, 500)
        self.assertGreater(config.LARGURA_TELA, 0)
        self.assertGreater(config.ALTURA_TELA, 0)

    def test_taxa_atualizacao_fps(self):
        self.assertEqual(config.FPS, 60)

    def test_cores_rgb(self):
        for nome_cor, cor in [
            ('COR_BRANCO', config.COR_BRANCO),
            ('COR_PRETO', config.COR_PRETO),
            ('COR_SERGIO', config.COR_SERGIO),
            ('COR_CLAUDIO', config.COR_CLAUDIO),
            ('COR_TEXTO_MENU', config.COR_TEXTO_MENU),
            ('COR_TEXTO_HUD', config.COR_TEXTO_HUD),
        ]:
            self.assertEqual(len(cor), 3, f"{nome_cor} deve ter 3 canais (R, G, B)")
            for canal in cor:
                self.assertTrue(0 <= canal <= 255, f"Canal de {nome_cor} fora do intervalo [0, 255]: {canal}")

    def test_parametros_jogabilidade(self):
        self.assertGreater(config.VELOCIDADE_INICIAL, 0)
        self.assertGreater(config.TAMANHO_INICIAL, 0)
        self.assertGreater(config.RAIO_CENTOPEIA, 0)
        self.assertEqual(config.PONTUACAO_VITORIA_MODO_CURTO, 30)


class TestPrevencaoAutoColisao(unittest.TestCase):
    """Testes para validar a logica de prevencao de auto-colisao imediata (Issue #26)."""

    def setUp(self):
        self.direcoes_opostas = {
            'ESQUERDA': 'DIREITA',
            'DIREITA': 'ESQUERDA',
            'CIMA': 'BAIXO',
            'BAIXO': 'CIMA',
        }

    def processar_comando(self, direcao_atual, proxima_direcao, novo_comando):
        """Replica a logica implementada no loop de eventos do main.py."""
        if novo_comando is not None:
            if (self.direcoes_opostas.get(novo_comando) != direcao_atual and
                self.direcoes_opostas.get(novo_comando) != proxima_direcao):
                return novo_comando
        return proxima_direcao

    def test_bloqueia_inversao_direta(self):
        """Centopeia indo para DIREITA deve ignorar comando imediato para ESQUERDA."""
        direcao_atual = 'DIREITA'
        proxima_direcao = 'DIREITA'
        resultado = self.processar_comando(direcao_atual, proxima_direcao, 'ESQUERDA')
        self.assertEqual(resultado, 'DIREITA', "Comando oposto imediato nao deve ser aceito")

    def test_permite_mudanca_ortogonal(self):
        """Centopeia indo para DIREITA deve aceitar comando para CIMA ou BAIXO."""
        direcao_atual = 'DIREITA'
        proxima_direcao = 'DIREITA'
        self.assertEqual(self.processar_comando(direcao_atual, proxima_direcao, 'CIMA'), 'CIMA')
        self.assertEqual(self.processar_comando(direcao_atual, proxima_direcao, 'BAIXO'), 'BAIXO')

    def test_bloqueia_giro_rapido_180_no_mesmo_frame(self):
        """
        Ao pressionar CIMA e rapidamente ESQUERDA no mesmo frame (partindo de DIREITA):
        1) CIMA e aceito;
        2) ESQUERDA deve ser rejeitado pois e oposto a direcao_atual (DIREITA).
        """
        direcao_atual = 'DIREITA'
        proxima_direcao = 'DIREITA'
        # Primeiro comando no mesmo frame:
        proxima_direcao = self.processar_comando(direcao_atual, proxima_direcao, 'CIMA')
        self.assertEqual(proxima_direcao, 'CIMA')
        # Segundo comando rapido no mesmo frame:
        proxima_direcao = self.processar_comando(direcao_atual, proxima_direcao, 'ESQUERDA')
        self.assertEqual(proxima_direcao, 'CIMA', "Segundo comando oposto a direcao_atual deve ser rejeitado")

    def test_bloqueia_segundo_comando_oposto_ao_primeiro_no_mesmo_frame(self):
        """
        Ao pressionar CIMA e rapidamente BAIXO no mesmo frame (partindo de DIREITA):
        1) CIMA e aceito;
        2) BAIXO deve ser rejeitado pois e oposto a proxima_direcao agendada (CIMA).
        """
        direcao_atual = 'DIREITA'
        proxima_direcao = 'DIREITA'
        proxima_direcao = self.processar_comando(direcao_atual, proxima_direcao, 'CIMA')
        self.assertEqual(proxima_direcao, 'CIMA')
        proxima_direcao = self.processar_comando(direcao_atual, proxima_direcao, 'BAIXO')
        self.assertEqual(proxima_direcao, 'CIMA', "Comando oposto a proxima_direcao agendada deve ser rejeitado")


class TestComida(unittest.TestCase):
    """Testes para validar o instanciamento e sorteio da comida (Food)."""

    def setUp(self):
        self.food = Bib_Centopid.Food(100, 100)

    def test_instanciacao_comida(self):
        """Verifica se a comida e instanciada com posicao, rect e tipo valido."""
        self.assertIsNotNone(self.food.rect)
        self.assertEqual(self.food.rect.topleft, (100, 100))
        self.assertIn(self.food.tipo, ['normal', 'especial', 'bonus'])
        self.assertIn(self.food.pontos, [1, 3, 5])

    def test_sortear_posicao(self):
        """Verifica se sortear_posicao reposiciona a comida dentro dos limites da tela."""
        self.food.sortear_posicao()
        self.assertTrue(0 <= self.food.rect.x <= config.LARGURA_TELA - self.food.rect.width)
        self.assertTrue(0 <= self.food.rect.y <= config.ALTURA_TELA - self.food.rect.height)
        self.assertIn(self.food.tipo, ['normal', 'especial', 'bonus'])


if __name__ == '__main__':
    unittest.main()
