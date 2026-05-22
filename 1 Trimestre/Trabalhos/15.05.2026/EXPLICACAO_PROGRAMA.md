# Explicação detalhada — Player simples (main.py)

## Visão geral
Este programa é um reprodutor de áudio simples feito com `pygame`. Ele carrega músicas locais de uma pasta (`Musicas.MP3` ou `Musicas`), reproduz a faixa atual, exibe uma interface gráfica com a capa do álbum e controles básicos (anterior/próxima/play-pause e ajuste de volume). Inclui também um fundo desfocado gerado a partir da própria capa para melhorar a aparência.

## Arquivo
- Local: `1 Trimestre/Trabalhos/15.05.2026/main.py`
- Arquivo de apoio: capa em `IMG/` (variável `IMAGEM_CAPA`).

## Como executar
1. Instale o `pygame` (por exemplo: `pip install pygame`).
2. Coloque suas músicas em `Musicas.MP3` ou `Musicas` na mesma pasta do `main.py`.
3. Execute:

```bash
python "1 Trimestre/Trabalhos/15.05.2026/main.py"
```

## Principais constantes e configurações
- `IMAGEM_CAPA`: caminho para a imagem exibida como capa.
- `PASTAS_MUSICA`: lista de pastas buscadas para localizar arquivos de áudio.
- Cores: várias constantes `COR_*` para permitir tema escuro/claro.

## Fluxo de execução
1. O programa busca a pasta de músicas via `achar_pasta_musicas()`.
2. Carrega todas as faixas suportadas (`.mp3`, `.wav`, `.ogg`) em `carregar_musicas()` e ordena a playlist.
3. Inicializa `pygame` e o mixer, configura volume inicial e cria a janela.
4. Carrega a primeira faixa com `carregar_faixa(0)`.
5. Entra no loop principal onde desenha a interface e processa eventos (teclado e fim da faixa).

## Funções principais
- `achar_pasta_musicas() -> str | None`:
  - Procura as pastas listadas em `PASTAS_MUSICA` e retorna o primeiro caminho válido.

- `carregar_musicas() -> list[str]`:
  - Gera a lista de arquivos de áudio suportados na pasta encontrada.

- `carregar_faixa(indice: int) -> None`:
  - Atualiza `estado.indice`, carrega a faixa no `pygame.mixer.music`, inicia reprodução e atualiza o título da janela.

- `criar_fundo_desfocado(caminho: str, tamanho: tuple[int,int]) -> pygame.Surface`:
  - Gera uma versão desfocada da imagem da capa por downscale/upscale (simula blur).
  - Usa cache (`_fundo_cache`) para não recalcular enquanto o tamanho não mudar.
  - Aplica um overlay semitransparente para melhorar contraste do texto.

- `carregar_imagem(caminho: str, tamanho: tuple[int,int]) -> pygame.Surface`:
  - Faz `smoothscale` da imagem para caber na área solicitada e preserva transparência.

- `barra_progresso(surface, x, y, largura, altura, valor)`:
  - Desenha a barra de progresso com sombra e preenchimento baseado em `valor`.

- `desenhar_botoes_controle(surface, centro, tamanho, cor_fundo, cor_icone, pausado)`:
  - Desenha os botões (anterior, play/pause, próximo) em alta resolução numa surface temporária e depois faz `smoothscale` para manter qualidade ao redimensionar.

## Estado e UI
- `Estado` (dataclass): guarda `indice` (faixa atual), `volume`, `tema_escuro` e `pausado`.
- A interface exibe:
  - Título do app, subtítulo, nome da faixa atual, índice da faixa, volume atual.
  - Capa do álbum com moldura e um fundo desfocado atrás para profundidade.
  - Controles visuais (botões desenhados) — atualmente apenas visuais; o controle real é via teclado.

## Controles de teclado
- `→`: próxima faixa (`carregar_faixa(estado.indice + 1)`).
- `←`: faixa anterior (`carregar_faixa(estado.indice - 1)`).
- `↑`: aumenta volume em 10% (até 100%).
- `↓`: diminui volume em 10% (até 0%).
- `Espaço`: alterna entre pause/unpause.
- `T`: alterna tema claro/escuro.
- `Esc`: encerra o programa.

## Observações de desempenho e qualidade visual
- O fundo desfocado é gerado apenas quando o tamanho muda (cache), evitando trabalho desnecessário a cada frame.
- Os ícones de controle são desenhados em uma surface maior (`escala`) e reduzidos com `smoothscale` para preservar bordas suaves quando a janela muda de tamanho.
- A renderização usa `pygame.transform.smoothscale` para melhor qualidade de escalonamento.

## Possíveis melhorias (próximos passos)
- Tornar os botões clicáveis: detectar `pygame.MOUSEBUTTONDOWN` e as áreas dos botões para executar ações.
- Mostrar a posição atual da faixa (tempo decorrido / total) usando `pygame.mixer.music.get_pos()` e metadados.
- Animações sutis (hover, clique) nos botões.
- Exportar a lista de músicas para um arquivo de playlist.

## Problemas comuns e depuração
- Erro ao carregar o mixer: verifique se `pygame` está instalado e o backend de áudio do sistema está disponível.
- Nenhuma música encontrada: confirme a presença de arquivos na pasta `Musicas.MP3` ou `Musicas`.
- Imagem de capa ausente: o programa substitui por uma superfície semitransparente de fallback.

---
Se quiser, eu adiciono detecção de clique nos botões e atualizo o `main.py` para suportar interação com o mouse. Também posso traduzir este arquivo para `README.md` na raiz do projeto.
