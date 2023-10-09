import pygame
import os
import random

TELA_LARGURA= 500
TELA_ALTURA= 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))
IMAGEM_CHAO =  pygame.transform.scale2x(pygame.image.load('imgs/base.png'))
IMAGEM_FUNDO =  pygame.transform.scale2x(pygame.image.load('imgs/bg.png'))
IMAGEM_PASSAROS = (
 pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')),
 pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')),
 pygame.transform.scale2x(pygame.image.load('imgs/bird3.png')),
)

pygame.font.init()
FONTES_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:

    IMGS= IMAGEM_PASSAROS
    ROTACAO_MAXIMA=25
    VELOCIDADE_ROTACAO=20
    TEMPO_ANIMACAO=5

    def __init__(self, x, y, angulo, velocidade):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = velocidade
        self.altura= y
        self.contagem_imagem= 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade= -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.velocidade+=1
        ##revisar calculo do deslocamento
        deslocamento = 1.5 * (self.tempo **2) + self.velocidade * self.tempo
        #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento =- 2

        self.y =+ deslocamento

        #o angulo do passáro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo = self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem+= 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < (self.TEMPO_ANIMACAO * 2):
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < (self.TEMPO_ANIMACAO * 3):
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < (self.TEMPO_ANIMACAO * 4):
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem > self.TEMPO_ANIMACAO *4 +1:
            self.imagem = self.IMGS[0]

        if self.angulo <= 80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        ##desenhar o passaro
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_center_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_center_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
       pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA= 200
    VELOCIDADE = 5

    def __init__(self, x):
        ##altura do cano será aleatória
        self.x = x
        self.altura = 0
        #esta posicao do cano de cima
        self.posicao_topo = 0
        self.posicao_base = 0
        self.CANO_BASE = IMAGEM_CANO
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura= random.randrange(50,450)
        self.posicao_topo = self.altura -  self.CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA


    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_BASE, (self.x, self.posicao_base))
        tela.blit(self.CANO_TOPO, (self.x, self.posicao_topo))

    def colidir(self, passaro):
        passaro_mask= passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        ##calcula a distancia no topo para o passaro
        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))
        #retorna verdadeiro se existe um ponto de colisão
        topo_ponto = topo_mask.overlap(passaro_mask, distancia_topo)
        base_ponto = base_mask.overlap(passaro_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True

        return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.LARGURA
        self.x2 -= self.LARGURA

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x1 +  self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 =  self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, chao, canos, pontos):
    tela.blit(IMAGEM_FUNDO, (0, 0))

