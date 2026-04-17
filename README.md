# Aulas de Algoritmo

Este repositório reúne exercícios introdutórios em Python do 1º trimestre.

## Objetivo geral

Praticar lógica de programação, entrada e saída de dados, operações matemáticas, estruturas de repetição e manipulação de textos.

## Estrutura dos arquivos

### 1 Trimestre/Trabalhos/17.04.2026/main.py

**Como foi feito:**
- Player musical com `pygame` e playlist automática (`.mp3` e `.ogg`) na pasta `Musicas`.
- Interface em estilo app com card principal, imagem de capa (`IMG/marshmello-material-3840x2160-26106.png`) e HUD.
- Layout ajustável com janela redimensionável e título da faixa com ajuste de fonte/quebra de linha para caber no layout.
- Fundo com cores aleatórias da paleta do projeto e atualização em `5 FPS`.
- Troca automática de música ao final da faixa com evento `MUSIC_END`.

**Por que é usado:**
- Praticar manipulação de áudio com `pygame.mixer.music`.
- Treinar organização de interface e responsividade em Pygame.
- Trabalhar eventos de teclado, estados do player e renderização por frame.

**Controles:**
- `↑ / ↓`: volume ±0.1
- `P`: pausar
- `R`: retomar
- `→ / ←`: próxima/anterior
- `S`: parar e sair

---

### 1 Trimestre/30 de março de 2026/Main.py

**Como foi feito:**
- Interface musical com `pygame` em estilo moderno (tema escuro com acentos dourados).
- Layout responsivo com altura mínima de 600px e painéis em efeito glassmorphism.
- Player com capa da faixa, barra de progresso, controle de volume e indicadores de estado.
- Sistema de playlist lendo automaticamente todos os arquivos `.mp3` da pasta `Violino Metal`.
- Troca de faixa por teclado e avanço automático quando a música termina.
- LED animado sincronizado com estado de reprodução (para quando a música pausa).

**Por que é usado:**
- Praticar estruturação de um projeto maior com funções separadas por responsabilidade.
- Aplicar manipulação de áudio e interface gráfica em tempo real com `pygame`.
- Treinar eventos de teclado, atualização por frame e estado de aplicação.

---

### 1 Trimestre/9 de março de 2026/aula01.py

**Como foi feito:**
- Programa em laço `while True` para registrar compras sucessivas.
- Menu textual com opções para combustíveis, loja de conveniência e finalização.
- Uso de condicionais `if/elif/else` para definir preço por produto.
- Cálculo de subtotal e total geral com acumuladores.

**Por que é usado:**
- Treinar controle de fluxo com menu interativo.
- Simular um cenário real de atendimento (posto de gasolina).
- Praticar cálculos financeiros e formatação de valores em reais.

---

### 1 Trimestre/23 de março de 2026/aula02-part1.py

**Como foi feito:**
- Leitura de dois números com `input()` e conversão para `float`.
- Cálculo das operações básicas: soma, subtração, multiplicação, divisão, resto e potência.
- Leitura de nome e aplicação de funções de string (`len`, `upper`, `lower`, `title`).

**Por que é usado:**
- Reforçar operações aritméticas em Python.
- Entender tipos numéricos e conversão de dados.
- Introduzir manipulação básica de strings.

---

### 1 Trimestre/23 de março de 2026/aula02-part2.py

**Como foi feito:**
- Captura de uma entrada textual do usuário.
- Exibição do tipo do dado com `type()`.
- Aplicação de métodos de validação de string (`isspace`, `isnumeric`, `isdecimal`, `isdigit`, `isalpha`, `isalnum`, `isupper`, `islower`, `istitle`).
- Transformações de texto (`upper`, `lower`, `strip`) e contagem de caracteres com `len`.

**Por que é usado:**
- Compreender como analisar entradas do teclado.
- Identificar características do conteúdo digitado.
- Praticar métodos úteis para validação e limpeza de dados.

---

### 1 Trimestre/25 de março de 2026/aula03-part1.py

**Como foi feito:**
- Jogo 2D com `pygame`, janela `800x600` e loop principal.
- Classe `PACMAN` com posição, direção e atualização por frame.
- Controle por teclado com setas para movimentação.
- Ação especial de **turbo** ao segurar `ESPAÇO`.
- Desenho do personagem com círculo, boca e olho usando `pygame.draw`.
- Limites de tela para impedir que o personagem saia da área visível.

**Por que é usado:**
- Introduzir programação orientada a objetos em jogos.
- Praticar eventos de teclado e atualização contínua de tela.
- Entender lógica de movimento e colisão com bordas.

---

### 1 Trimestre/25 de março de 2026/aula03-part2.py

**Como foi feito:**
- Uso do módulo `math` para operações matemáticas.
- Leitura de número inteiro com `input()`.
- Cálculo de raiz quadrada, arredondamento para cima/baixo e potência.

**Por que é usado:**
- Praticar biblioteca padrão de matemática.
- Reforçar entrada de dados e formatação de saída.

---

### 1 Trimestre/25 de março de 2026/aula03-parte3.py

**Como foi feito:**
- Uso do módulo `random` para sorteios.
- Sorteio de número inteiro entre 1 e 10.
- Sorteio de nomes de alunos e embaralhamento de lista.

**Por que é usado:**
- Introduzir geração de aleatoriedade em Python.
- Praticar listas, separação de texto e iteração com `for`.

## Requisitos

- Python 3 instalado.
- Biblioteca `pygame` para executar o jogo em `1 Trimestre/25 de março de 2026/aula03-part1.py`.
- Biblioteca `pygame` para executar os players em:
	- `1 Trimestre/30 de março de 2026/Main.py`
	- `1 Trimestre/Trabalhos/17.04.2026/main.py`

## Como executar

1. Abra a pasta do projeto no VS Code.
2. Execute qualquer arquivo `.py` individualmente.
3. Siga as perguntas exibidas no terminal.

### Execução do jogo (aula03-part1.py)

1. Instale o Pygame:
	- `pip install pygame`
2. Execute o arquivo `1 Trimestre/25 de março de 2026/aula03-part1.py`.
3. Controles:
	- Setas: movimentação
	- Espaço: turbo

### Execução do player (Trabalho 17.04.2026)

1. Instale o Pygame:
	- `pip install pygame`
2. Coloque músicas `.mp3` ou `.ogg` em `1 Trimestre/Trabalhos/17.04.2026/Musicas`.
3. Execute o arquivo `1 Trimestre/Trabalhos/17.04.2026/main.py`.
4. Controles:
	- Seta para cima/baixo: aumentar/diminuir volume
	- P: pausar
	- R: retomar
	- Seta para direita/esquerda: próxima/anterior
	- S: sair

### Execução do player Music Lounge (Main.py - 30/03)

1. Instale o Pygame:
	- `pip install pygame`
2. Execute o arquivo `1 Trimestre/30 de março de 2026/Main.py`.
3. Controles:
	- Espaço: play/pause
	- P: pausar
	- R: retomar
	- T: reiniciar faixa atual
	- N: próxima faixa
	- B: faixa anterior
	- Seta para esquerda/direita: retroceder/avançar 5 segundos
	- Seta para cima/baixo: aumentar/diminuir volume
	- H: expandir/recolher atalhos
	- S: sair

## Autor

Luís Fernando
