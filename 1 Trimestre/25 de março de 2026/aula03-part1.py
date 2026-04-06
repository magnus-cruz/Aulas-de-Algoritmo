import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VELOCIDADE = 1

class PACMAN:
    def __init__(self):
        self.linha = 1
        self.coluna = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = 800 // 30
        self.dir_x = 0
        self.dir_y = 0
        self.turbo_ativo = False
        self.raio = self.tamanho // 2

    def calcular_regras(self):
        velocidade_atual = VELOCIDADE * (2 if self.turbo_ativo else 1)
        self.coluna = self.coluna + (self.dir_x * velocidade_atual)
        self.linha = self.linha + (self.dir_y * velocidade_atual)
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

        if self.centro_x + self.raio > 800:
            self.centro_x = 800 - self.raio
        if self.centro_x - self.raio < 0:
            self.centro_x = self.raio
        if self.centro_y + self.raio > 600:
            self.centro_y = 600 - self.raio
        if self.centro_y - self.raio < 0:
            self.centro_y = self.raio

        self.coluna = (self.centro_x - self.raio) / self.tamanho
        self.linha = (self.centro_y - self.raio) / self.tamanho

    def processar_event(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.dir_x = 1
                elif e.key == pygame.K_LEFT:
                    self.dir_x = -1
                elif e.key == pygame.K_UP:
                    self.dir_y = -1
                elif e.key == pygame.K_DOWN:
                    self.dir_y = 1
                elif e.key == pygame.K_SPACE:
                    self.turbo_ativo = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    if self.dir_x == 1:
                        self.dir_x = 0
                elif e.key == pygame.K_LEFT:
                    if self.dir_x == -1:
                        self.dir_x = 0
                elif e.key == pygame.K_UP:
                    if self.dir_y == -1:
                        self.dir_y = 0
                elif e.key == pygame.K_DOWN:
                    if self.dir_y == 1:
                        self.dir_y = 0
                elif e.key == pygame.K_SPACE:
                    self.turbo_ativo = False

    def processar_eventos_mouse(self, ev):
        delay = 1000
        for e in ev:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay

    def pintar(self, tela):
        #Desenhar o corpo do PACMAN
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        #Desenho da boca do PACMAN
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_infeior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_infeior]

        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #Olho do PACMAN
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

if __name__ == '__main__':
    pacman = PACMAN()

    while True:
        #1º Calculas as regras
        pacman.calcular_regras()


        #2º Pintar a tela
        screen.fill((PRETO))
        pacman.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        #3º Captura os eventos.
        ev = pygame.event.get()
        for e in ev:
            if e.type == pygame.QUIT:
                exit()
        pacman.processar_event(ev)