"""
Módulo de configuração do jogo Centopid.
Centraliza constantes de dimensões, taxas de atualização, cores e parâmetros de jogabilidade.
Atende à Issue #30 cadastrada por @tuannycristinef.
"""

# Dimensões da janela / tela do jogo
LARGURA_TELA = 800
ALTURA_TELA = 500

# Taxa de atualização (FPS)
FPS = 60

# Cores no formato RGB
COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)
COR_SERGIO = (44, 44, 44)         # Skin 0: Sérgio (cinza escuro)
COR_CLAUDIO = (126, 20, 186)      # Skin 1: Cláudio (roxo)
COR_TEXTO_MENU = (110, 75, 24)    # Marrom escuro para recorde no menu inicial
COR_TEXTO_HUD = (161, 115, 66)    # Marrom claro para texto da interface em jogo (HUD)

# Parâmetros de jogabilidade
VELOCIDADE_INICIAL = 2.5
INCREMENTO_VELOCIDADE = 0.2
TAMANHO_INICIAL = 2
INCREMENTO_TAMANHO = 2
RAIO_CENTOPEIA = 15
PONTUACAO_VITORIA_MODO_CURTO = 30
