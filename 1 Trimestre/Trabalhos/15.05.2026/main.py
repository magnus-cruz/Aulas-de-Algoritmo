import glob
import os
import sys
from dataclasses import dataclass
    
import pygame


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGEM_CAPA = os.path.join(BASE_DIR, "IMG", "michael-jackson-colorful-art-gsy24mm3qlfpzi63.jpg")
PASTAS_MUSICA = [
    os.path.join(BASE_DIR, "Musicas.MP3"),
    os.path.join(BASE_DIR, "Musicas"),
]

COR_FUNDO_ESCURO = (20, 28, 48)
COR_FUNDO_CLARO = (240, 240, 245)
COR_CARD_ESCURO = (32, 40, 60)
COR_CARD_CLARO = (255, 255, 255)
COR_TEXTO_ESCURO = (245, 245, 245)
COR_TEXTO_CLARO = (18, 18, 18)
COR_SECUNDARIA_ESCURO = (180, 190, 205)
COR_SECUNDARIA_CLARO = (120, 128, 145)
COR_DESTAQUE = (210, 65, 65)
COR_AZUL = (54, 84, 134)


def achar_pasta_musicas() -> str | None:
    for pasta in PASTAS_MUSICA:
        if os.path.isdir(pasta):
            return pasta
    return None


def carregar_musicas() -> list[str]:
    pasta = achar_pasta_musicas()
    if pasta is None:
        return []

    musicas: list[str] = []
    musicas.extend(glob.glob(os.path.join(pasta, "*.mp3")))
    musicas.extend(glob.glob(os.path.join(pasta, "*.wav")))
    musicas.extend(glob.glob(os.path.join(pasta, "*.ogg")))
    return sorted(musicas)


playlist = carregar_musicas()
if not playlist:
    print("Nenhuma música encontrada na pasta Musicas.MP3 ou Musicas.")
    sys.exit(1)


@dataclass
class Estado:
    indice: int = 0
    volume: float = 0.7
    tema_escuro: bool = True
    pausado: bool = False


estado = Estado()

pygame.init()
pygame.mixer.init()
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.set_volume(estado.volume)

tela = pygame.display.set_mode((1000, 650), pygame.RESIZABLE)
pygame.display.set_caption("Player simples")
clock = pygame.time.Clock()


def nome_da_musica(caminho: str) -> str:
    return os.path.splitext(os.path.basename(caminho))[0]


def fonte(tamanho: int, negrito: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui", tamanho, bold=negrito)


def desenhar_texto(
    surface: pygame.Surface,
    frase: str,
    f: pygame.font.Font,
    cor,
    posicao,
    centro: bool = False,
) -> None:
    imagem = f.render(frase, True, cor)
    rect = imagem.get_rect()
    if centro:
        rect.center = posicao
    else:
        rect.topleft = posicao
    surface.blit(imagem, rect)


def carregar_faixa(indice: int) -> None:
    estado.indice = indice % len(playlist)
    pygame.mixer.music.load(playlist[estado.indice])
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(estado.volume)
    estado.pausado = False
    pygame.display.set_caption(f"Player simples - {nome_da_musica(playlist[estado.indice])}")


def alternar_tema() -> None:
    estado.tema_escuro = not estado.tema_escuro


def cor_fundo() -> tuple[int, int, int]:
    return COR_FUNDO_ESCURO if estado.tema_escuro else COR_FUNDO_CLARO


def cor_card() -> tuple[int, int, int]:
    return COR_CARD_ESCURO if estado.tema_escuro else COR_CARD_CLARO


def cor_texto() -> tuple[int, int, int]:
    return COR_TEXTO_ESCURO if estado.tema_escuro else COR_TEXTO_CLARO


def cor_secundaria() -> tuple[int, int, int]:
    return COR_SECUNDARIA_ESCURO if estado.tema_escuro else COR_SECUNDARIA_CLARO


def barra_progresso(surface: pygame.Surface, x: int, y: int, largura: int, altura: int, valor: float) -> None:
    # Sombra
    pygame.draw.rect(surface, (30, 30, 30), (x+3, y+3, largura, altura), border_radius=altura // 2)
    # Barra de fundo
    pygame.draw.rect(surface, (70, 78, 95), (x, y, largura, altura), border_radius=altura // 2)
    # Barra de progresso
    pygame.draw.rect(surface, COR_DESTAQUE, (x, y, int(largura * valor), altura), border_radius=altura // 2)

def desenhar_botoes_controle(surface: pygame.Surface, centro: tuple[int, int], tamanho: int, cor_fundo, cor_icone, pausado: bool):
    # Desenha ícones em alta resolução numa surface temporária e aplica smoothscale
    escala = 4
    espacamento = int(tamanho * 1.6)
    temp_w = int((tamanho * 6 + espacamento * 2) * escala)
    temp = pygame.Surface((temp_w, temp_w), pygame.SRCALPHA)
    cx = temp_w // 2
    cy = temp_w // 2

    r = int(tamanho * escala)
    esp = int(espacamento * escala)

    # Anterior (duas setas)
    pygame.draw.circle(temp, cor_fundo, (cx - esp, cy), r)
    pygame.draw.polygon(temp, cor_icone, [
        (cx - esp + 12 * escala, cy),
        (cx - esp + r // 2, cy - r // 2 + 6 * escala),
        (cx - esp + r // 2, cy + r // 2 - 6 * escala),
    ])
    pygame.draw.polygon(temp, cor_icone, [
        (cx - esp - 6 * escala, cy),
        (cx - esp + 8 * escala, cy - r // 2 + 6 * escala),
        (cx - esp + 8 * escala, cy + r // 2 - 6 * escala),
    ])

    # Play / Pause
    pygame.draw.circle(temp, cor_fundo, (cx, cy), r)
    if pausado:
        pygame.draw.polygon(temp, cor_icone, [
            (cx - 8 * escala, cy - 18 * escala), (cx + 18 * escala, cy), (cx - 8 * escala, cy + 18 * escala)
        ])
    else:
        pygame.draw.rect(temp, cor_icone, (cx - 10 * escala, cy - 16 * escala, 8 * escala, 32 * escala), border_radius=4 * escala)
        pygame.draw.rect(temp, cor_icone, (cx + 4 * escala, cy - 16 * escala, 8 * escala, 32 * escala), border_radius=4 * escala)

    # Próximo (duas setas)
    pygame.draw.circle(temp, cor_fundo, (cx + esp, cy), r)
    pygame.draw.polygon(temp, cor_icone, [
        (cx + esp - 12 * escala, cy),
        (cx + esp - r // 2, cy - r // 2 + 6 * escala),
        (cx + esp - r // 2, cy + r // 2 - 6 * escala),
    ])
    pygame.draw.polygon(temp, cor_icone, [
        (cx + esp + 6 * escala, cy),
        (cx + esp - 8 * escala, cy - r // 2 + 6 * escala),
        (cx + esp - 8 * escala, cy + r // 2 - 6 * escala),
    ])

    final = pygame.transform.smoothscale(temp, (int(temp_w / escala), int(temp_w / escala)))
    fx = int(centro[0] - final.get_width() // 2)
    fy = int(centro[1] - final.get_height() // 2)
    surface.blit(final, (fx, fy))


def carregar_imagem(caminho: str, tamanho: tuple[int, int]) -> pygame.Surface:
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
    except pygame.error:
        superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
        superficie.fill((255, 255, 255, 20))
        return superficie

    largura_imagem, altura_imagem = imagem.get_size()
    escala = min(tamanho[0] / largura_imagem, tamanho[1] / altura_imagem)
    nova_largura = max(1, int(largura_imagem * escala))
    nova_altura = max(1, int(altura_imagem * escala))
    imagem = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))

    superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
    superficie.blit(imagem, imagem.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2)))
    return superficie


# Cache para fundo desfocado (reutiliza até o tamanho mudar)
_fundo_cache = None
_fundo_cache_size: tuple[int, int] = (0, 0)


def criar_fundo_desfocado(caminho: str, tamanho: tuple[int, int]) -> pygame.Surface:
    """Gera um fundo desfocado a partir da imagem original usando down/upscale para simular blur."""
    global _fundo_cache, _fundo_cache_size
    if _fundo_cache and _fundo_cache_size == tamanho:
        return _fundo_cache

    try:
        img = pygame.image.load(caminho).convert_alpha()
    except pygame.error:
        s = pygame.Surface(tamanho, pygame.SRCALPHA)
        s.fill((30, 30, 30, 255))
        _fundo_cache = s
        _fundo_cache_size = tamanho
        return s

    w, h = img.get_size()
    escala_cover = max(tamanho[0] / w, tamanho[1] / h)
    img = pygame.transform.smoothscale(img, (max(1, int(w * escala_cover)), max(1, int(h * escala_cover))))

    # Criar versão pequena e reescalar para simular blur
    pequeno = pygame.transform.smoothscale(img, (max(1, int(tamanho[0] * 0.06)), max(1, int(tamanho[1] * 0.06))))
    desfocado = pygame.transform.smoothscale(pequeno, tamanho)

    superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
    superficie.blit(desfocado, (0, 0))

    # Overlay para contraste com tema
    overlay = pygame.Surface(tamanho, pygame.SRCALPHA)
    overlay.fill((10, 14, 24, 140) if estado.tema_escuro else (255, 255, 255, 80))
    superficie.blit(overlay, (0, 0))

    _fundo_cache = superficie
    _fundo_cache_size = tamanho
    return superficie


try:
    carregar_faixa(0)
except pygame.error as erro:
    print(f"Erro ao abrir a primeira música: {erro}")
    pygame.quit()
    sys.exit(1)


rodando = True
while rodando:
    largura, altura = tela.get_size()
    tela.fill(cor_fundo())

    pygame.draw.circle(tela, COR_DESTAQUE, (int(largura * 0.12), int(altura * 0.18)), 80)
    pygame.draw.circle(tela, COR_AZUL, (int(largura * 0.86), int(altura * 0.18)), 110)

    card = pygame.Rect(60, 50, largura - 120, altura - 100)
    sombra = card.move(8, 10)
    pygame.draw.rect(tela, (0, 0, 0), sombra, border_radius=30)
    pygame.draw.rect(tela, cor_card(), card, border_radius=30)

    imagem_tamanho = (240, 240)
    imagem = carregar_imagem(IMAGEM_CAPA, imagem_tamanho)
    imagem_rect = imagem.get_rect()
    imagem_rect.topleft = (card.x + 30, card.y + 110)

    # Fundo desfocado para dar profundidade atrás da capa
    fundo_tamanho = (imagem_tamanho[0] + 60, imagem_tamanho[1] + 60)
    fundo = criar_fundo_desfocado(IMAGEM_CAPA, fundo_tamanho)
    fundo_rect = fundo.get_rect()
    fundo_rect.topleft = (imagem_rect.x - 15, imagem_rect.y - 15)
    tela.blit(fundo, fundo_rect)

    # Moldura branca ao redor (com leve inflate)
    pygame.draw.rect(tela, (255, 255, 255), imagem_rect.inflate(10, 10), border_radius=22)
    tela.blit(imagem, imagem_rect)

    titulo = fonte(28, True)
    normal = fonte(22)
    pequeno = fonte(16)
    grande = fonte(34, True)

    desenhar_texto(tela, "Player simples", titulo, COR_DESTAQUE, (card.x + 30, card.y + 25))
    desenhar_texto(
        tela,
        "Sem links, só música local e visual básico.",
        pequeno,
        cor_secundaria(),
        (card.x + 30, card.y + 65),
    )

    musica = nome_da_musica(playlist[estado.indice])
    texto_x = card.x + 320
    desenhar_texto(tela, musica, grande, cor_texto(), (texto_x, card.y + 150))
    desenhar_texto(
        tela,
        f"Faixa {estado.indice + 1} de {len(playlist)}",
        normal,
        cor_secundaria(),
        (texto_x, card.y + 205),
    )
    desenhar_texto(
        tela,
        f"Volume: {int(estado.volume * 100)}%",
        normal,
        cor_secundaria(),
        (texto_x, card.y + 245),
    )

    barra_progresso(tela, texto_x, card.y + 295, card.right - texto_x - 40, 18, estado.volume)

    # Botões de controle
    botoes_centro = (texto_x + 180, card.y + 400)
    desenhar_botoes_controle(
        tela,
        botoes_centro,
        32,
        (60, 60, 80) if estado.tema_escuro else (220, 220, 230),
        COR_DESTAQUE,
        estado.pausado
    )

    # Detalhe gráfico extra: linhas decorativas
    pygame.draw.line(tela, COR_AZUL, (card.x + 20, card.bottom - 40), (card.right - 20, card.bottom - 40), 3)
    pygame.draw.line(tela, COR_DESTAQUE, (card.x + 20, card.bottom - 35), (card.right - 20, card.bottom - 35), 1)

    status = "Pausado" if estado.pausado else "Tocando"
    status_cor = COR_DESTAQUE if estado.pausado else (120, 220, 140)
    desenhar_texto(tela, status, fonte(24, True), status_cor, (texto_x, card.y + 345))

    desenhar_texto(
        tela,
        "Controles: ← anterior | → próxima | ↑ volume | ↓ volume | espaço pausa | T tema | Esc sair",
        pequeno,
        cor_texto(),
        (card.x + 30, card.bottom - 70),
    )

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            elif evento.key == pygame.K_RIGHT:
                carregar_faixa(estado.indice + 1)
            elif evento.key == pygame.K_LEFT:
                carregar_faixa(estado.indice - 1)
            elif evento.key == pygame.K_UP:
                estado.volume = min(1.0, estado.volume + 0.1)
                pygame.mixer.music.set_volume(estado.volume)
            elif evento.key == pygame.K_DOWN:
                estado.volume = max(0.0, estado.volume - 0.1)
                pygame.mixer.music.set_volume(estado.volume)
            elif evento.key == pygame.K_SPACE:
                if estado.pausado:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                estado.pausado = not estado.pausado
            elif evento.key == pygame.K_t:
                alternar_tema()
        elif evento.type == MUSIC_END:
            carregar_faixa(estado.indice + 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()