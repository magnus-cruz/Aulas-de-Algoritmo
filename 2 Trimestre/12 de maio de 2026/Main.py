import pygame
import random


pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 600, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Genius - O Jogo da Memória")


FUNDO = (30, 30, 30)
BRANCO = (255, 255, 255)
CINZA = (150, 150, 150)

CORES_NORMAIS = {
    0: (0, 120, 0),    # Verde Escuro
    1: (120, 0, 0),    # Vermelho Escuro
    2: (150, 150, 0),  # Amarelo Escuro
    3: (0, 0, 120)     # Azul Escuro
}

CORES_ACESAS = {
    0: (50, 255, 50),  # Verde Brilhante
    1: (255, 50, 50),  # Vermelho Brilhante
    2: (255, 255, 50), # Amarelo Brilhante

    3: (50, 50, 255)   # Azul Brilhante
}

fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)


sons = {}
try:
    sons[0] = pygame.mixer.Sound('verde.wav')
    sons[1] = pygame.mixer.Sound('vermelho.wav')
    sons[2] = pygame.mixer.Sound('amarelo.wav')
    sons[3] = pygame.mixer.Sound('azul.wav')
    som_erro = pygame.mixer.Sound('erro.wav')
    sons_carregados = True
except FileNotFoundError:
    print("Aviso: Arquivos de áudio não encontrados. O jogo rodará sem som.")
    sons_carregados = False

def tocar_som(id_cor):
    if sons_carregados:
        sons[id_cor].play()


tamanho_botao = 200
espacamento = 20
centro_x, centro_y = LARGURA // 2, ALTURA // 2


botoes = {
    0: pygame.Rect(centro_x - tamanho_botao - espacamento, centro_y - tamanho_botao - espacamento, tamanho_botao, tamanho_botao),
    1: pygame.Rect(centro_x + espacamento, centro_y - tamanho_botao - espacamento, tamanho_botao, tamanho_botao),
    2: pygame.Rect(centro_x - tamanho_botao - espacamento, centro_y + espacamento, tamanho_botao, tamanho_botao),
    3: pygame.Rect(centro_x + espacamento, centro_y + espacamento, tamanho_botao, tamanho_botao)
}

sequencia = []

cliques_do_jogador = 0
estado = "MENU" # Estados: MENU, MOSTRANDO_SEQUENCIA, VEZ_DO_JOGADOR, GAME_OVER
pontuacao = 0

def desenhar_interface(botao_aceso=None):
    tela.fill(FUNDO)
   

    for i, rect in botoes.items():
        cor = CORES_ACESAS[i] if i == botao_aceso else CORES_NORMAIS[i]
        # border_radius deixa os botões com cantos arredondados (design moderno)
        pygame.draw.rect(tela, cor, rect, border_radius=20)
       

    if estado == "MENU":
        texto = fonte_titulo.render("Clique para Iniciar", True, BRANCO)
    elif estado == "GAME_OVER":
        texto = fonte_titulo.render(f"Fim de Jogo! Pontos: {pontuacao}", True, BRANCO)
        texto2 = fonte_pequena.render("Clique em qualquer lugar para reiniciar", True, CINZA)
        tela.blit(texto2, (LARGURA//2 - texto2.get_width()//2, 50))
    else:
        texto = fonte_titulo.render(f"Pontuação: {pontuacao}", True, BRANCO)

    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 15))
    pygame.display.flip()

def adicionar_cor_e_mostrar():
    global estado
    estado = "MOSTRANDO_SEQUENCIA"
    sequencia.append(random.randint(0, 3))
   
    pygame.time.delay(1000) # Pausa dramática antes de começar a mostrar
   
    for cor_id in sequencia:
        # Acende o botão
        desenhar_interface(botao_aceso=cor_id)
        tocar_som(cor_id)
        pygame.time.delay(500) # Tempo que a luz fica acesa
       
        # Apaga o botão
        desenhar_interface()
        pygame.time.delay(250) # Pausa entre as luzes
       

    pygame.event.clear()
    estado = "VEZ_DO_JOGADOR"
# Loop principal do jogo
rodando = True
while rodando:
    # Desenha a interface do jogo
    desenhar_interface()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == "MENU":
                pontuacao = 0
                sequencia.clear()
                adicionar_cor_e_mostrar()
            elif estado == "VEZ_DO_JOGADOR":
                pos = pygame.mouse.get_pos()
                for cor_id, rect in botoes.items():
                    if rect.collidepoint(pos):
                        tocar_som(cor_id)
                        if cor_id == sequencia[cliques_do_jogador]:
                            cliques_do_jogador += 1
                            if cliques_do_jogador == len(sequencia):
                                pontuacao += 1
                                cliques_do_jogador = 0
                                adicionar_cor_e_mostrar()
                else:
                    if sons_carregados:
                        som_erro.play()
                        estado = "GAME_OVER"
            elif estado == "GAME_OVER":
                pontuacao = 0
                sequencia.clear()
                cliques_do_jogador = 0
                estado = "MENU"
            