import pygame
import sys
import random
import math

# Inicialização
pygame.init()

# Tela
LARGURA, ALTURA = 600, 600
TAMANHO = 20
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha Estilizada 🐍")

# Cores
AZUL = (0, 102, 255)
VERDE_CLARO = (170, 215, 81)
VERDE_ESCURO = (162, 209, 73)
VERMELHO = (255, 0, 0)
VERDE_TALO = (0, 200, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Fonte personalizada
fonte_pontos = pygame.font.Font(pygame.font.match_font('freesansbold'), 28)
fonte_mensagem = pygame.font.Font(pygame.font.match_font('freesansbold'), 50)
fonte_sub = pygame.font.Font(pygame.font.match_font('freesansbold'), 30)

clock = pygame.time.Clock()
FPS = 10

def nova_posicao():
    return (
        random.randint(0, (LARGURA - TAMANHO) // TAMANHO) * TAMANHO,
        random.randint(0, (ALTURA - TAMANHO) // TAMANHO) * TAMANHO,
    )

def desenhar_tabuleiro():
    for y in range(0, ALTURA, TAMANHO):
        for x in range(0, LARGURA, TAMANHO):
            cor = VERDE_CLARO if (x // TAMANHO + y // TAMANHO) % 2 == 0 else VERDE_ESCURO
            pygame.draw.rect(tela, cor, (x, y, TAMANHO, TAMANHO))

def desenhar_cobra(cobra, direcao):
    for i, (x, y) in enumerate(cobra):
        if i == 0:
            centro = (x + TAMANHO // 2, y + TAMANHO // 2)
            pygame.draw.circle(tela, AZUL, centro, TAMANHO // 2)

            # Ligação com o corpo
            if len(cobra) > 1:
                x2, y2 = cobra[1]
                dx = x2 - x
                dy = y2 - y
                if dx != 0:
                    rect_x = x + TAMANHO // 2 if dx < 0 else x2 + TAMANHO // 2
                    pygame.draw.rect(tela, AZUL, (rect_x, y, TAMANHO // 2, TAMANHO))
                elif dy != 0:
                    rect_y = y + TAMANHO // 2 if dy < 0 else y2 + TAMANHO // 2
                    pygame.draw.rect(tela, AZUL, (x, rect_y, TAMANHO, TAMANHO // 2))

            # Olhos
            olho_tam = 4
            if direcao == (TAMANHO, 0):
                olho1 = (centro[0] + 4, centro[1] - 4)
                olho2 = (centro[0] + 4, centro[1] + 4)
            elif direcao == (-TAMANHO, 0):
                olho1 = (centro[0] - 4, centro[1] - 4)
                olho2 = (centro[0] - 4, centro[1] + 4)
            elif direcao == (0, TAMANHO):
                olho1 = (centro[0] - 4, centro[1] + 4)
                olho2 = (centro[0] + 4, centro[1] + 4)
            else:
                olho1 = (centro[0] - 4, centro[1] - 4)
                olho2 = (centro[0] + 4, centro[1] - 4)
            pygame.draw.circle(tela, BRANCO, olho1, olho_tam)
            pygame.draw.circle(tela, BRANCO, olho2, olho_tam)
            pygame.draw.circle(tela, PRETO, olho1, 2)
            pygame.draw.circle(tela, PRETO, olho2, 2)
        else:
            pygame.draw.rect(tela, AZUL, (x, y, TAMANHO, TAMANHO))

def desenhar_maca(pos, pulsar):
    centro = (pos[0] + TAMANHO // 2, pos[1] + TAMANHO // 2)
    raio = TAMANHO // 2 + pulsar
    pygame.draw.circle(tela, VERMELHO, centro, raio)
    talo = pygame.Rect(centro[0] - 2, centro[1] - raio - 6, 4, 6)
    pygame.draw.rect(tela, VERDE_TALO, talo)

def mostrar_mensagem(texto, subtitulo=""):
    tela.fill((20, 20, 20))  # Fundo escuro

    msg = fonte_mensagem.render(texto, True, (255, 60, 60))
    sub = fonte_sub.render(subtitulo, True, (200, 200, 200))

    msg_rect = msg.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
    sub_rect = sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 20))

    tela.blit(msg, msg_rect)
    tela.blit(sub, sub_rect)
    pygame.display.flip()

def jogo():
    cobra = [(300, 300)]
    direcao = (0, 0)
    maca = nova_posicao()
    pontos = 0
    pausado = False
    tick = 0

    while True:
        tick += 1
        pulsar = int(math.sin(tick * 0.2) * 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w and direcao != (0, TAMANHO): direcao = (0, -TAMANHO)
                elif evento.key == pygame.K_s and direcao != (0, -TAMANHO): direcao = (0, TAMANHO)
                elif evento.key == pygame.K_a and direcao != (TAMANHO, 0): direcao = (-TAMANHO, 0)
                elif evento.key == pygame.K_d and direcao != (-TAMANHO, 0): direcao = (TAMANHO, 0)
                elif evento.key == pygame.K_ESCAPE: pausado = not pausado

        if pausado:
            mostrar_mensagem("PAUSADO", "Pressione ESC para continuar")
            continue

        if direcao != (0, 0):
            nova = (cobra[0][0] + direcao[0], cobra[0][1] + direcao[1])
            cobra.insert(0, nova)
            if cobra[0] == maca:
                pontos += 1
                maca = nova_posicao()
            else:
                cobra.pop()

        if (
            cobra[0][0] < 0 or cobra[0][0] >= LARGURA or
            cobra[0][1] < 0 or cobra[0][1] >= ALTURA or
            cobra[0] in cobra[1:]
        ):
            mostrar_mensagem(f"Game Over! Pontos: {pontos}", "R = reiniciar | Q = sair")
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            return jogo()
                        elif evento.key == pygame.K_q:
                            pygame.quit(); sys.exit()

        desenhar_tabuleiro()
        desenhar_cobra(cobra, direcao)
        desenhar_maca(maca, pulsar)

        texto = fonte_pontos.render(f"Pontos: {pontos}", True, PRETO)
        tela.blit(texto, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Iniciar o jogo
jogo()
