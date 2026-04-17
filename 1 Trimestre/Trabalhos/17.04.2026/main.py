import glob
import os
import random
import sys

import pygame


# Paleta obrigatória do exercício
GUNMETAL = (71, 68, 72)    # #474448
SHADOW_GREY = (45, 35, 46)  # #2d232e
BONE = (224, 221, 207)      # #e0ddcf
TAUPE_GREY = (83, 75, 82)   # #534b52
PARCHMENT = (241, 240, 234) # #f1f0ea
PALETA = [GUNMETAL, SHADOW_GREY, BONE, TAUPE_GREY, PARCHMENT]


# Diretório das músicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_MUSICAS = os.path.join(BASE_DIR, "Musicas")


# Lê todos os arquivos suportados na pasta Musicas/
playlist = sorted(
    glob.glob(os.path.join(PASTA_MUSICAS, "*.mp3")) +
    glob.glob(os.path.join(PASTA_MUSICAS, "*.ogg"))
)

if not playlist:
    print("Erro: nenhuma música .mp3 ou .ogg foi encontrada na pasta Musicas/.")
    sys.exit(1)


# Estado do player
index = 0
volume = 0.7
MUSIC_END = pygame.USEREVENT + 1


# Inicialização do Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(MUSIC_END)

largura, altura = 1180, 720
screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
pygame.display.set_caption(f"{os.path.splitext(os.path.basename(playlist[index]))[0]} | Vol: {volume:.0%}")
clock = pygame.time.Clock()
NOME_FONTE = "segoeui"
fonte_titulo = pygame.font.SysFont(NOME_FONTE, 54, bold=True)
fonte_info = pygame.font.SysFont("segoeui", 28)
fonte_rodape = pygame.font.SysFont("segoeui", 22)
fonte_micro = pygame.font.SysFont("segoeui", 18)


def carregar_capa(caminho: str, tamanho: tuple[int, int]) -> pygame.Surface:
    """Carrega e ajusta a imagem da capa para caber no card."""
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
    except pygame.error:
        superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
        superficie.fill((255, 255, 255, 18))
        return superficie

    largura_img, altura_img = imagem.get_size()
    escala = min(tamanho[0] / largura_img, tamanho[1] / altura_img)
    nova_largura = max(1, int(largura_img * escala))
    nova_altura = max(1, int(altura_img * escala))
    imagem = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))

    superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
    ret = imagem.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2))
    superficie.blit(imagem, ret)
    return superficie


def desenhar_retangulo_ondulado(superficie: pygame.Surface, cor, rect, raio: int = 26, alpha: int | None = None) -> None:
    """Desenha um retângulo arredondado com ou sem transparência."""
    if alpha is None:
        pygame.draw.rect(superficie, cor, rect, border_radius=raio)
        return

    caixa = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (*cor, alpha), caixa.get_rect(), border_radius=raio)
    superficie.blit(caixa, rect.topleft)


def desenhar_texto(texto: str, fonte: pygame.font.Font, cor, posicao, centro: bool = False) -> pygame.Rect:
    """Renderiza e desenha um texto retornando seu retângulo."""
    render = fonte.render(texto, True, cor)
    ret = render.get_rect()
    if centro:
        ret.center = posicao
    else:
        ret.topleft = posicao
    screen.blit(render, ret)
    return ret


def ajustar_fonte_para_largura(texto: str, fonte_base: pygame.font.Font, largura_maxima: int, altura_maxima: int | None = None) -> pygame.font.Font:
    """Reduz a fonte até o texto caber na largura e, opcionalmente, na altura."""
    tamanho = fonte_base.get_height()
    while tamanho >= 18:
        fonte_teste = pygame.font.SysFont(NOME_FONTE, tamanho, bold=fonte_base.get_bold(), italic=fonte_base.get_italic())
        render = fonte_teste.render(texto, True, (255, 255, 255))
        cabe_altura = altura_maxima is None or render.get_height() <= altura_maxima
        if render.get_width() <= largura_maxima and cabe_altura:
            return fonte_teste
        tamanho -= 1
    return pygame.font.SysFont(NOME_FONTE, 18, bold=fonte_base.get_bold(), italic=fonte_base.get_italic())


def quebrar_texto(texto: str, fonte: pygame.font.Font, largura_maxima: int, max_linhas: int = 2) -> list[str]:
    """Quebra o texto em linhas que caibam na largura informada."""
    palavras = texto.split()
    if not palavras:
        return [texto]

    linhas: list[str] = []
    linha_atual = palavras[0]

    for palavra in palavras[1:]:
        tentativa = f"{linha_atual} {palavra}"
        if fonte.size(tentativa)[0] <= largura_maxima:
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    linhas.append(linha_atual)

    if len(linhas) <= max_linhas:
        return linhas

    linhas = linhas[:max_linhas]
    ultima = linhas[-1]
    while ultima and fonte.size(ultima + "...")[0] > largura_maxima:
        ultima = ultima[:-1].rstrip()
    linhas[-1] = f"{ultima}..." if ultima else "..."
    return linhas


def nome_da_faixa(caminho: str) -> str:
    """Retorna apenas o nome do arquivo, sem extensão."""
    return os.path.splitext(os.path.basename(caminho))[0]


def atualizar_cabecalho() -> None:
    """Atualiza o título da janela com faixa atual e volume."""
    pygame.display.set_caption(f"{nome_da_faixa(playlist[index])} | Vol: {volume:.0%}")


def tocar_faixa(novo_index: int) -> None:
    """Carrega e inicia a reprodução da faixa indicada."""
    global index
    index = novo_index % len(playlist)
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    atualizar_cabecalho()


def barra_volume(superficie: pygame.Surface, x: int, y: int, largura_barra: int, altura_barra: int, valor: float) -> None:
    """Desenha uma barra de volume com preenchimento proporcional."""
    pygame.draw.rect(superficie, (255, 255, 255, 26), (x, y, largura_barra, altura_barra), border_radius=altura_barra // 2)
    preenchimento = int(largura_barra * valor)
    if preenchimento > 0:
        pygame.draw.rect(superficie, BONE, (x, y, preenchimento, altura_barra), border_radius=altura_barra // 2)


# Inicia a primeira música da playlist
try:
    tocar_faixa(index)
except pygame.error as erro:
    print(f"Erro ao tocar a música inicial: {erro}")
    pygame.quit()
    sys.exit(1)


# Texto fixo do rodapé com os controles
rodape = [
    "Controles:",
    "↑ / ↓ volume",
    "P pausar",
    "R retomar",
    "S parar e sair",
    "→ próxima faixa",
    "← faixa anterior",
]

imagem_capa = carregar_capa(
    os.path.join(BASE_DIR, "IMG", "marshmello-material-3840x2160-26106.png"),
    (340, 340),
)

icone_controles = [
    ("↑", "Aumenta"),
    ("↓", "Diminui"),
    ("P", "Pausa"),
    ("R", "Play"),
    ("→", "Próxima"),
    ("←", "Anterior"),
]


executando = True
while executando:
    largura_tela, altura_tela = screen.get_size()

    # Fundo aleatório da paleta a cada frame
    cor_fundo = random.choice(PALETA)
    screen.fill(cor_fundo)

    # Camada suave para dar aparência de app moderno
    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    pygame.draw.circle(overlay, (255, 255, 255, 18), (int(largura_tela * 0.22), int(altura_tela * 0.18)), 190)
    pygame.draw.circle(overlay, (0, 0, 0, 24), (int(largura_tela * 0.88), int(altura_tela * 0.18)), 240)
    screen.blit(overlay, (0, 0))

    # Card principal com sombra
    margem = 46
    card = pygame.Rect(margem, margem, largura_tela - (margem * 2), altura_tela - (margem * 2))
    sombra = card.copy()
    sombra.x += 10
    sombra.y += 14
    desenhar_retangulo_ondulado(screen, (0, 0, 0), sombra, raio=34, alpha=92)
    desenhar_retangulo_ondulado(screen, (255, 255, 255), card, raio=34, alpha=42)

    # Bloco da capa com moldura
    capa_tamanho = min(390, card.height - 128)
    capa_fundo = pygame.Rect(card.x + 34, card.y + 34, capa_tamanho, capa_tamanho)
    desenhar_retangulo_ondulado(screen, (255, 255, 255), capa_fundo, raio=30, alpha=22)
    screen.blit(imagem_capa, imagem_capa.get_rect(center=capa_fundo.center))

    # Gradiente simples para destacar o conteúdo da direita
    destaque = pygame.Surface((max(1, card.width - (capa_fundo.right - card.x) - 40), card.height - 68), pygame.SRCALPHA)
    for i in range(destaque.get_width()):
        alpha = int(55 * (1 - i / max(1, destaque.get_width())))
        pygame.draw.line(destaque, (255, 255, 255, alpha), (i, 0), (i, destaque.get_height()))
    screen.blit(destaque, (capa_fundo.right + 26, card.y + 34))

    # Lida com eventos do teclado e do fim da música
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == MUSIC_END:
            tocar_faixa(index + 1)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
                atualizar_cabecalho()
            elif evento.key == pygame.K_DOWN:
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)
                atualizar_cabecalho()
            elif evento.key == pygame.K_p:
                pygame.mixer.music.pause()
            elif evento.key == pygame.K_r:
                pygame.mixer.music.unpause()
            elif evento.key == pygame.K_s:
                pygame.mixer.music.stop()
                executando = False
            elif evento.key == pygame.K_RIGHT:
                tocar_faixa(index + 1)
            elif evento.key == pygame.K_LEFT:
                tocar_faixa(index - 1)

    # HUD principal
    nome_faixa = nome_da_faixa(playlist[index])
    total_faixas = len(playlist)
    numero_faixa = f"{index + 1:02d} / {total_faixas:02d}"
    texto_volume = f"Volume: {volume:.0%}"

    lado_direito_x = capa_fundo.right + 34
    topo_texto = card.y + 82
    largura_texto_max = card.right - lado_direito_x - 34

    desenhar_texto("TOCANDO AGORA", fonte_micro, TAUPE_GREY, (lado_direito_x, topo_texto))
    fonte_nome = ajustar_fonte_para_largura(nome_faixa, fonte_titulo, largura_texto_max, 150)
    linhas_nome = quebrar_texto(nome_faixa, fonte_nome, largura_texto_max, max_linhas=2)
    y_nome = topo_texto + 30
    for linha in linhas_nome:
        desenhar_texto(linha, fonte_nome, GUNMETAL, (lado_direito_x, y_nome))
        y_nome += fonte_nome.get_linesize() + 4

    y_info = max(topo_texto + 120, y_nome + 10)
    desenhar_texto(f"Faixa {numero_faixa}", fonte_info, SHADOW_GREY, (lado_direito_x, y_info))
    desenhar_texto(texto_volume, fonte_info, SHADOW_GREY, (lado_direito_x, y_info + 45))

    # Barra de volume e informações visuais
    barra_volume(screen, lado_direito_x, y_info + 96, largura_texto_max, 22, volume)
    desenhar_texto("Volume", fonte_micro, TAUPE_GREY, (lado_direito_x, y_info + 128))

    # Botões visuais dos controles
    botao_x = lado_direito_x
    botao_y = y_info + 172
    for indice_botao, (atalho, legenda) in enumerate(icone_controles):
        coluna = indice_botao % 2
        linha = indice_botao // 2
        largura_botao = min(220, (largura_texto_max - 20) // 2)
        bx = botao_x + coluna * (largura_botao + 20)
        by = botao_y + linha * 74
        ret_botao = pygame.Rect(bx, by, largura_botao, 54)
        desenhar_retangulo_ondulado(screen, GUNMETAL, ret_botao, raio=18, alpha=170)
        desenhar_texto(atalho, fonte_info, PARCHMENT, (bx + 22, by + 11))
        desenhar_texto(legenda, fonte_rodape, BONE, (bx + 72, by + 16))

    # Rodapé com dica curta
    faixa_rodape = pygame.Rect(card.x + 34, card.bottom - 92, card.width - 68, 56)
    desenhar_retangulo_ondulado(screen, SHADOW_GREY, faixa_rodape, raio=18, alpha=120)
    desenhar_texto("S fecha o player • setas navegam na playlist • P pausa • R retoma", fonte_rodape, PARCHMENT, (faixa_rodape.x + 18, faixa_rodape.y + 15))

    # Texto auxiliar discreto para manter a legibilidade do layout
    desenhar_texto(rodape[0], fonte_micro, TAUPE_GREY, (card.x + 34, card.bottom - 138))

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
