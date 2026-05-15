import glob
import io
import os
import random
import sys
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import urlopen

import pygame


# Paleta do exercício
MOLTEN_LAVA = (120, 0, 0)
BRICK_RED = (193, 18, 31)
PAPAYA_WHIP = (253, 240, 213)
DEEP_SPACE_BLUE = (0, 48, 73)
STEEL_BLUE = (102, 155, 188)

WHITE = (255, 255, 255)

PALETA_TEMA = {
    "dark": {
        "bg": DEEP_SPACE_BLUE,
        "bg_alt": MOLTEN_LAVA,
        "card": (0, 0, 0, 214),
        "card_edge": (255, 255, 255, 20),
        "text": PAPAYA_WHIP,
        "muted": STEEL_BLUE,
        "muted_2": PAPAYA_WHIP,
        "accent": BRICK_RED,
        "accent_2": STEEL_BLUE,
        "bar_bg": (255, 255, 255, 30),
        "bar_fill": BRICK_RED,
        "button": (25, 25, 25, 210),
        "button_border": (255, 255, 255, 18),
        "button_text": PAPAYA_WHIP,
    },
    "light": {
        "bg": PAPAYA_WHIP,
        "bg_alt": STEEL_BLUE,
        "card": (255, 255, 255, 220),
        "card_edge": (0, 0, 0, 16),
        "text": DEEP_SPACE_BLUE,
        "muted": DEEP_SPACE_BLUE,
        "muted_2": BRICK_RED,
        "accent": MOLTEN_LAVA,
        "accent_2": STEEL_BLUE,
        "bar_bg": (0, 0, 0, 20),
        "bar_fill": BRICK_RED,
        "button": (255, 255, 255, 220),
        "button_border": (0, 0, 0, 16),
        "button_text": DEEP_SPACE_BLUE,
    },
}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIVEIS_PASTAS = [
    os.path.join(BASE_DIR, "Musicas"),
    os.path.join(BASE_DIR, "Musicas.MP3"),
]
ARQUIVO_LINKS = os.path.join(BASE_DIR, "links.txt")


def encontrar_pasta_musicas() -> str:
    for pasta in POSSIVEIS_PASTAS:
        if os.path.isdir(pasta):
            return pasta
    return POSSIVEIS_PASTAS[0]


PASTA_MUSICAS = encontrar_pasta_musicas()


def carregar_playlist_local() -> list[str]:
    return sorted(
        glob.glob(os.path.join(PASTA_MUSICAS, "*.mp3"))
        + glob.glob(os.path.join(PASTA_MUSICAS, "*.ogg"))
        + glob.glob(os.path.join(PASTA_MUSICAS, "*.wav"))
    )


def carregar_playlist_links() -> list[str]:
    if not os.path.exists(ARQUIVO_LINKS):
        return []

    links: list[str] = []
    with open(ARQUIVO_LINKS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            url = linha.strip()
            if not url or url.startswith("#"):
                continue
            if url.startswith(("http://", "https://")):
                links.append(url)
    return links


def is_url(origem: str) -> bool:
    return origem.startswith(("http://", "https://"))


def carregar_playlist_por_modo(modo: str) -> list[str]:
    if modo == "links":
        links = carregar_playlist_links()
        if links:
            return links
    return carregar_playlist_local()


playlist = carregar_playlist_por_modo("links" if carregar_playlist_links() else "local")

if not playlist:
    print("Erro: nenhuma música compatível foi encontrada na pasta de músicas nem em links.txt.")
    sys.exit(1)


@dataclass
class EstadoApp:
    indice: int = 0
    volume: float = 0.72
    tema: str = "dark"
    pausado: bool = False
    modo_fonte: str = "local"
    mensagem: str = ""
    mensagem_expira: int = 0


estado = EstadoApp()
estado.modo_fonte = "links" if carregar_playlist_links() else "local"
MUSIC_END = pygame.USEREVENT + 1
buffer_audio_atual: io.BytesIO | None = None


pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(MUSIC_END)

screen = pygame.display.set_mode((1280, 760), pygame.RESIZABLE)
pygame.display.set_caption("Michael Jackson Player")
clock = pygame.time.Clock()


def nome_da_faixa(caminho: str) -> str:
    if is_url(caminho):
        parsed = urlparse(caminho)
        nome = os.path.splitext(os.path.basename(parsed.path))[0]
        return nome or parsed.netloc or "Faixa online"
    return os.path.splitext(os.path.basename(caminho))[0]


def tema_atual() -> dict:
    return PALETA_TEMA[estado.tema]


def ajustar_superficie_imagem(caminho: str, tamanho: tuple[int, int]) -> pygame.Surface:
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
    superficie.blit(imagem, imagem.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2)))
    return superficie


def carregar_capa() -> pygame.Surface:
    candidatos = [
        os.path.join(BASE_DIR, "IMG", "michael-jackson-colorful-art-gsy24mm3qlfpzi63.jpg"),
    ]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return caminho
    return ajustar_superficie_imagem(os.path.join(BASE_DIR, "IMG", "capa.png"), (600, 600))


CAPA = carregar_capa()
if isinstance(CAPA, str):
    imagem_capa_original = CAPA
else:
    imagem_capa_original = None
    imagem_capa = CAPA


def redimensionar_capa(tamanho: tuple[int, int]) -> pygame.Surface:
    if imagem_capa_original:
        return ajustar_superficie_imagem(imagem_capa_original, tamanho)
    return pygame.transform.smoothscale(imagem_capa, tamanho)


def carregar_fonte(nome: str, tamanho: int, bold: bool = False, italic: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont(nome, tamanho, bold=bold, italic=italic)


def fonte_responsiva(base: int, tela_largura: int, multiplicador: float, minimo: int, maximo: int) -> int:
    return max(minimo, min(maximo, int(base + tela_largura * multiplicador)))


def desenhar_texto(superficie: pygame.Surface, texto: str, fonte: pygame.font.Font, cor, posicao, centro: bool = False) -> pygame.Rect:
    render = fonte.render(texto, True, cor)
    ret = render.get_rect()
    if centro:
        ret.center = posicao
    else:
        ret.topleft = posicao
    superficie.blit(render, ret)
    return ret


def desenhar_retangulo_ondulado(superficie: pygame.Surface, cor, rect: pygame.Rect, raio: int = 24, alpha: int | None = None) -> None:
    if alpha is None:
        pygame.draw.rect(superficie, cor, rect, border_radius=raio)
        return
    caixa = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (*cor, alpha), caixa.get_rect(), border_radius=raio)
    superficie.blit(caixa, rect.topleft)


def ajustar_fonte_para_largura(texto: str, fonte_base: pygame.font.Font, largura_maxima: int, altura_maxima: int | None = None) -> pygame.font.Font:
    tamanho = fonte_base.get_height()
    while tamanho >= 18:
        fonte_teste = carregar_fonte("segoeui", tamanho, bold=fonte_base.get_bold(), italic=fonte_base.get_italic())
        render = fonte_teste.render(texto, True, WHITE)
        cabe_altura = altura_maxima is None or render.get_height() <= altura_maxima
        if render.get_width() <= largura_maxima and cabe_altura:
            return fonte_teste
        tamanho -= 1
    return carregar_fonte("segoeui", 18, bold=fonte_base.get_bold(), italic=fonte_base.get_italic())


def quebrar_texto(texto: str, fonte: pygame.font.Font, largura_maxima: int, max_linhas: int = 2) -> list[str]:
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


def atualizar_cabecalho() -> None:
    pygame.display.set_caption(
        f"Michael Jackson Player | {nome_da_faixa(playlist[estado.indice])} | Vol {estado.volume:.0%} | {estado.tema.title()} | {estado.modo_fonte.title()}"
    )


def mostrar_mensagem(texto: str, duracao_ms: int = 2400) -> None:
    estado.mensagem = texto
    estado.mensagem_expira = pygame.time.get_ticks() + duracao_ms


def preparar_origem_audio(origem: str) -> None:
    global buffer_audio_atual
    if is_url(origem):
        with urlopen(origem) as resposta:
            buffer_audio_atual = io.BytesIO(resposta.read())
        extensao = os.path.splitext(urlparse(origem).path)[1].lstrip(".")
        pygame.mixer.music.load(buffer_audio_atual, namehint=extensao or "mp3")
        return

    buffer_audio_atual = None
    pygame.mixer.music.load(origem)


def tocar_faixa(novo_indice: int) -> None:
    if not playlist:
        raise pygame.error("A playlist está vazia.")

    inicio = novo_indice
    tentativas = 0
    ultimo_erro: Exception | None = None

    while tentativas < len(playlist):
        estado.indice = inicio % len(playlist)
        origem = playlist[estado.indice]
        try:
            preparar_origem_audio(origem)
            pygame.mixer.music.set_volume(estado.volume)
            pygame.mixer.music.play()
            estado.pausado = False
            atualizar_cabecalho()
            return
        except Exception as erro:
            ultimo_erro = erro
            inicio += 1
            tentativas += 1

    raise pygame.error(f"Não foi possível reproduzir a playlist: {ultimo_erro}")


def alternar_tema() -> None:
    estado.tema = "light" if estado.tema == "dark" else "dark"
    atualizar_cabecalho()


def alternar_fonte_playlist() -> None:
    global playlist

    if estado.modo_fonte == "local":
        links = carregar_playlist_links()
        if links:
            estado.modo_fonte = "links"
            playlist = links
            estado.indice %= len(playlist)
            tocar_faixa(estado.indice)
            mostrar_mensagem("Modo links ativado")
        else:
            mostrar_mensagem("Adicione URLs em links.txt para usar o modo links")
        return

    playlist_local = carregar_playlist_local()
    if not playlist_local:
        mostrar_mensagem("Nenhuma faixa local encontrada")
        return

    estado.modo_fonte = "local"
    playlist = playlist_local
    estado.indice %= len(playlist)
    tocar_faixa(estado.indice)
    mostrar_mensagem("Modo local ativado")


def barra_progresso(superficie: pygame.Surface, x: int, y: int, largura_barra: int, altura_barra: int, valor: float, tema: dict) -> None:
    pygame.draw.rect(superficie, tema["bar_bg"], (x, y, largura_barra, altura_barra), border_radius=altura_barra // 2)
    preenchimento = int(largura_barra * max(0.0, min(1.0, valor)))
    if preenchimento > 0:
        pygame.draw.rect(superficie, tema["bar_fill"], (x, y, preenchimento, altura_barra), border_radius=altura_barra // 2)


try:
    tocar_faixa(estado.indice)
except pygame.error as erro:
    print(f"Erro ao tocar a música inicial: {erro}")
    pygame.quit()
    sys.exit(1)


icone_controles = [
    ("↑", "Volume +"),
    ("↓", "Volume -"),
    ("P", "Pausar"),
    ("R", "Retomar"),
    ("→", "Próxima"),
    ("←", "Anterior"),
    ("T", "Tema"),
]


executando = True
while executando:
    largura_tela, altura_tela = screen.get_size()
    tema = tema_atual()

    if largura_tela < 900:
        margem = max(20, int(min(largura_tela, altura_tela) * 0.03))
    else:
        margem = 44

    screen.fill(tema["bg"])
    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    pygame.draw.circle(overlay, (*tema["accent"], 30), (int(largura_tela * 0.14), int(altura_tela * 0.16)), max(120, int(min(largura_tela, altura_tela) * 0.16)))
    pygame.draw.circle(overlay, (*tema["accent_2"], 18), (int(largura_tela * 0.84), int(altura_tela * 0.2)), max(140, int(min(largura_tela, altura_tela) * 0.22)))
    pygame.draw.circle(overlay, (255, 255, 255, 10) if estado.tema == "dark" else (0, 0, 0, 8), (int(largura_tela * 0.5), int(altura_tela * 0.78)), max(180, int(min(largura_tela, altura_tela) * 0.25)))
    screen.blit(overlay, (0, 0))

    card = pygame.Rect(margem, margem, largura_tela - (margem * 2), altura_tela - (margem * 2))
    sombra = card.copy()
    sombra.x += max(8, margem // 3)
    sombra.y += max(10, margem // 2)
    desenhar_retangulo_ondulado(screen, DEEP_SPACE_BLUE, sombra, raio=36, alpha=90 if estado.tema == "dark" else 60)
    desenhar_retangulo_ondulado(screen, tema["card"], card, raio=36, alpha=None)
    desenhar_retangulo_ondulado(screen, tema["card_edge"], card, raio=36, alpha=None)

    topo_card = card.y + max(22, margem // 2)
    largura_util = card.width - max(40, margem)
    altura_util = card.height - max(40, margem)

    modo_vertical = largura_tela < 980
    if modo_vertical:
        capa_lado = min(int(largura_util * 0.78), int(altura_util * 0.36), 440)
        capa_rect = pygame.Rect(0, 0, capa_lado, capa_lado)
        capa_rect.centerx = card.centerx
        capa_rect.y = topo_card + 6
        area_texto = pygame.Rect(card.x + max(24, margem // 2), capa_rect.bottom + 22, card.width - max(48, margem), card.bottom - (capa_rect.bottom + 44))
    else:
        capa_lado = min(int(card.height - margem * 1.2), int(card.width * 0.34), 450)
        capa_rect = pygame.Rect(card.x + max(26, margem // 2), card.y + max(26, margem // 2), capa_lado, capa_lado)
        area_texto = pygame.Rect(capa_rect.right + max(24, margem // 2), capa_rect.y, card.right - capa_rect.right - max(30, margem // 2), capa_rect.height)

    sombra_capa = capa_rect.copy()
    sombra_capa.x += 8
    sombra_capa.y += 10
    desenhar_retangulo_ondulado(screen, DEEP_SPACE_BLUE, sombra_capa, raio=30, alpha=75 if estado.tema == "dark" else 35)
    desenhar_retangulo_ondulado(screen, tema["button"], capa_rect, raio=30, alpha=None)
    desenhar_retangulo_ondulado(screen, tema["button_border"], capa_rect, raio=30, alpha=None)

    capa = redimensionar_capa((capa_rect.width - 14, capa_rect.height - 14))
    screen.blit(capa, capa.get_rect(center=capa_rect.center))

    barra_titulo_y = card.y + max(18, margem // 2)
    barra_titulo = pygame.Rect(card.x + max(18, margem // 2), barra_titulo_y, card.width - max(36, margem), 42)
    desenhar_texto(screen, "MICHAEL JACKSON PLAYER", carregar_fonte("segoeui", fonte_responsiva(16, largura_tela, 0.004, 16, 28), bold=True), tema["accent"], (barra_titulo.x, barra_titulo.y))
    desenhar_texto(screen, "Modo claro/escuro: tecla T", carregar_fonte("segoeui", fonte_responsiva(12, largura_tela, 0.0025, 12, 20)), tema["muted"], (barra_titulo.right - 250, barra_titulo.y + 4))

    faixa_atual = nome_da_faixa(playlist[estado.indice])
    total_faixas = len(playlist)
    numero_faixa = f"{estado.indice + 1:02d} / {total_faixas:02d}"
    texto_volume = f"Volume: {estado.volume:.0%}"
    texto_tema = f"Tema: {estado.tema.title()}"
    texto_origem = f"Fonte: {estado.modo_fonte.title()}"
    texto_status = "Tocando" if not estado.pausado else "Pausado"

    fonte_micro = carregar_fonte("segoeui", fonte_responsiva(12, largura_tela, 0.0018, 12, 20))
    fonte_info = carregar_fonte("segoeui", fonte_responsiva(20, largura_tela, 0.0032, 18, 34))
    fonte_titulo = carregar_fonte("segoeui", fonte_responsiva(28, largura_tela, 0.008, 24, 60), bold=True)
    fonte_rodape = carregar_fonte("segoeui", fonte_responsiva(13, largura_tela, 0.002, 12, 22))

    cabecalho = "TOCANDO AGORA"
    desenhar_texto(screen, cabecalho, fonte_micro, tema["muted"], (area_texto.x, area_texto.y))

    fonte_nome = ajustar_fonte_para_largura(faixa_atual, fonte_titulo, area_texto.width, 170 if not modo_vertical else 140)
    linhas_nome = quebrar_texto(faixa_atual, fonte_nome, area_texto.width, max_linhas=2)
    y_nome = area_texto.y + 34
    for linha in linhas_nome:
        desenhar_texto(screen, linha, fonte_nome, tema["text"], (area_texto.x, y_nome))
        y_nome += fonte_nome.get_linesize() + 4

    y_info = max(area_texto.y + 126, y_nome + 10)
    desenhar_texto(screen, f"Faixa {numero_faixa}", fonte_info, tema["muted_2"], (area_texto.x, y_info))
    desenhar_texto(screen, texto_volume, fonte_info, tema["muted_2"], (area_texto.x, y_info + 38))
    desenhar_texto(screen, texto_tema, fonte_info, tema["muted_2"], (area_texto.x, y_info + 76))
    desenhar_texto(screen, texto_origem, fonte_info, tema["muted_2"], (area_texto.x, y_info + 114))
    desenhar_texto(screen, texto_status, fonte_info, tema["accent"], (area_texto.x, y_info + 152))

    largura_barra = max(160, area_texto.width)
    barra_progresso(screen, area_texto.x, y_info + 198, largura_barra, 20, estado.volume, tema)
    desenhar_texto(screen, "Volume", fonte_micro, tema["muted"], (area_texto.x, y_info + 226))

    botao_largura = max(140, min(240, (area_texto.width - 20) // 2 if modo_vertical else (area_texto.width - 28) // 2))
    botao_altura = 56
    botoes_por_linha = 2 if area_texto.width >= 520 else 1
    botao_gap_x = 16
    botao_gap_y = 16
    inicio_botoes_y = y_info + 264
    for indice_botao, (atalho, legenda) in enumerate(icone_controles):
        coluna = indice_botao % botoes_por_linha
        linha = indice_botao // botoes_por_linha
        bx = area_texto.x + coluna * (botao_largura + botao_gap_x)
        by = inicio_botoes_y + linha * (botao_altura + botao_gap_y)
        ret_botao = pygame.Rect(bx, by, botao_largura, botao_altura)
        desenhar_retangulo_ondulado(screen, tema["button"], ret_botao, raio=18, alpha=None)
        desenhar_retangulo_ondulado(screen, tema["button_border"], ret_botao, raio=18, alpha=None)
        desenhar_texto(screen, atalho, fonte_info, tema["accent"], (bx + 18, by + 11))
        desenhar_texto(screen, legenda, fonte_rodape, tema["button_text"], (bx + 66, by + 16))

    barra_rodape = pygame.Rect(card.x + max(18, margem // 2), card.bottom - max(74, margem), card.width - max(36, margem), 52)
    desenhar_retangulo_ondulado(screen, tema["bg_alt"], barra_rodape, raio=18, alpha=180 if estado.tema == "dark" else 150)
    desenhar_texto(
        screen,
        "Setas navegam • P pausa • R retoma • S sai • T tema • L links/local",
        fonte_rodape,
        tema["text"],
        (barra_rodape.x + 18, barra_rodape.y + 16),
    )

    micro_rodape = pygame.Rect(card.x + max(18, margem // 2), barra_rodape.y - 28, card.width - max(36, margem), 20)
    desenhar_texto(screen, "Layout ajusta automaticamente ao redimensionar a janela.", fonte_micro, tema["muted"], (micro_rodape.x, micro_rodape.y))

    if estado.mensagem and pygame.time.get_ticks() <= estado.mensagem_expira:
        aviso = carregar_fonte("segoeui", fonte_responsiva(12, largura_tela, 0.002, 12, 20), bold=True)
        largura_aviso = min(card.width - 70, max(220, aviso.size(estado.mensagem)[0] + 28))
        aviso_rect = pygame.Rect(card.centerx - largura_aviso // 2, barra_rodape.y - 72, largura_aviso, 28)
        desenhar_retangulo_ondulado(screen, tema["accent"], aviso_rect, raio=14, alpha=160 if estado.tema == "dark" else 120)
        desenhar_texto(screen, estado.mensagem, aviso, tema["text"], (aviso_rect.x + 14, aviso_rect.y + 6))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.VIDEORESIZE:
            largura = max(720, evento.w)
            altura = max(520, evento.h)
            screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        elif evento.type == MUSIC_END:
            tocar_faixa(estado.indice + 1)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                estado.volume = min(1.0, estado.volume + 0.1)
                pygame.mixer.music.set_volume(estado.volume)
                atualizar_cabecalho()
            elif evento.key == pygame.K_DOWN:
                estado.volume = max(0.0, estado.volume - 0.1)
                pygame.mixer.music.set_volume(estado.volume)
                atualizar_cabecalho()
            elif evento.key == pygame.K_p:
                pygame.mixer.music.pause()
                estado.pausado = True
                atualizar_cabecalho()
            elif evento.key == pygame.K_r:
                pygame.mixer.music.unpause()
                estado.pausado = False
                atualizar_cabecalho()
            elif evento.key == pygame.K_s:
                pygame.mixer.music.stop()
                executando = False
            elif evento.key == pygame.K_RIGHT:
                tocar_faixa(estado.indice + 1)
            elif evento.key == pygame.K_LEFT:
                tocar_faixa(estado.indice - 1)
            elif evento.key == pygame.K_t:
                alternar_tema()
            elif evento.key == pygame.K_l:
                alternar_fonte_playlist()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
