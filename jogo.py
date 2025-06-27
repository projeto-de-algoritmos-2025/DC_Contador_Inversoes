import pygame
import random
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 1200
ALTURA = 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Organizador de Caos - Contagem de Inversões")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (70, 130, 180)
VERDE = (50, 205, 50)
VERMELHO = (220, 20, 60)
AMARELO = (255, 215, 0)
CINZA = (128, 128, 128)
ROXO = (138, 43, 226)
LARANJA = (255, 165, 0)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)

# Fontes
FONTE_GRANDE = pygame.font.Font(None, 48)
FONTE_MEDIA = pygame.font.Font(None, 36)
FONTE_PEQUENA = pygame.font.Font(None, 24)
FONTE_MUITO_PEQUENA = pygame.font.Font(None, 18)
