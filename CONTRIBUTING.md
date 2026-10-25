# Guia de contribuição — Centopid

## Sobre o projeto

Este repositório contém o projeto Centopid, desenvolvido em Python. O código principal está na pasta `Centopid`.

## Estrutura do projeto

- `Centopid/main.py`: arquivo principal do jogo.
- `Centopid/Bib_Centopid.py`: módulo auxiliar do projeto.
- `Centopid/imagens/`: diretório destinado aos recursos gráficos.

## Preparação do ambiente

1. Instale uma versão do Python compatível com as dependências do projeto.
2. Abra o terminal na pasta principal do repositório.
3. Consulte o arquivo `requirements.txt`, caso esteja disponível, para identificar as dependências.
4. Instale as dependências usando uma versão do Python compatível com elas.

## Execução

O arquivo principal do jogo é `Centopid/main.py`. Para executá-lo, abra o terminal na pasta principal do repositório e utilize:

```powershell
python .\Centopid\main.py
```

A execução depende da instalação correta das bibliotecas e dos recursos necessários.

## Como contribuir

1. Crie uma branch específica para sua tarefa.
2. Faça uma alteração relacionada a uma issue do projeto.
3. Teste a alteração antes de enviá-la.
4. Registre a mudança em um commit com uma mensagem clara.
5. Envie a branch ao GitHub e abra um pull request para revisão.
6. Descreva no pull request o que foi alterado e qual issue foi atendida.

## Padrão de commits

Sempre que possível, utilize mensagens no padrão Conventional Commits, por exemplo:

- `docs: adiciona guia de contribuição`
- `fix: corrige comportamento do jogo`
- `feat: adiciona funcionalidade`

## Revisão

As alterações devem ser revisadas pela equipe antes de serem integradas à branch principal.