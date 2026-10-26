# Centopid

Centopid é um jogo desenvolvido em **Python** utilizando a biblioteca **Pygame**. O jogador controla uma centopeia que deve coletar alimentos, aumentar sua pontuação e evitar colisões com as paredes e com o próprio corpo.

## Funcionalidades

- Menu inicial.
- Seleção de personagem (skins).
- Dois modos de jogo:
  - Modo Curto (objetivo de 30 pontos).
  - Modo Infinito.
- Sistema de pontuação e recorde.
- Reinício da partida após derrota.
- Tela de vitória no modo curto.

## Estrutura do projeto

```text
Trabalho-GCS/
├── CONTRIBUTING.md
├── README.md
└── Centopid/
    ├── main.py
    ├── Bib_Centopid.py
    ├── imagens/
    └── __pycache__/
```

## Requisitos

- Python 3
- Pygame

### Instalar a biblioteca Pygame via terminal Linux(Ubuntu)
- sudo apt install -y python3-pygame
**obs:** O recomendado é instalar um ambiente virtual para que o linux não reclame, porem se for apenas para projetos academicos, a instalação via _sudo apt_ funciona muito bem. 

## Como executar

1. Clone o repositório.
2. Abra o terminal na pasta do projeto.
3. Instale o Pygame (caso necessário).
4. Execute:

```bash
python Centopid/main.py
```

## Controles

| Tecla | Função |
|--------|--------|
| W ou ↑ | Mover para cima |
| S ou ↓ | Mover para baixo |
| A ou ← | Mover para esquerda |
| D ou → | Mover para direita |
| R | Reiniciar após Game Over |
| E | Voltar ao menu inicial |

## Como contribuir

1. Crie uma branch para sua tarefa.
2. Faça as alterações necessárias.
3. Realize um commit utilizando mensagens semânticas.
4. Envie a branch para o GitHub.
5. Abra um Pull Request para revisão da equipe.

## Padrão de commits

O projeto adota o padrão **Conventional Commits**.

Exemplos:

```text
feat: adiciona nova funcionalidade
fix: corrige colisão da centopeia
docs: atualiza README
refactor: reorganiza funções auxiliares
```

## Tecnologias utilizadas

- Python
- Pygame
- Git
- GitHub

## Equipe

Projeto desenvolvido para a disciplina de **Gerência de Configuração de Software (GCS)**.