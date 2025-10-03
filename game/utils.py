import pygame
import math
import random

pygame.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
GRIS = (128, 128, 128)

def crear_pantalla():

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Asteroides Espaciales")
    return pantalla

def dibujar_texto_centrado(pantalla, texto, tamaño, color, y_pos):

    fuente = pygame.font.Font(None, tamaño)
    texto_surface = fuente.render(texto, True, color)
    texto_rect = texto_surface.get_rect()
    texto_rect.centerx = ANCHO_PANTALLA // 2
    texto_rect.y = y_pos
    pantalla.blit(texto_surface, texto_rect)

def dibujar_texto_centrado_completo(pantalla, texto, tamaño, color, x, y):

    fuente = pygame.font.Font(None, tamaño)
    texto_surface = fuente.render(texto, True, color)
    texto_rect = texto_surface.get_rect()
    texto_rect.centerx = x
    texto_rect.centery = y
    pantalla.blit(texto_surface, texto_rect)

def detectar_colision(rect1, rect2):

    return rect1.colliderect(rect2)

def crear_asteroide_aleatorio():

    ancho_asteroide = random.randint(20, 50)
    alto_asteroide = random.randint(20, 50)
    x = random.randint(0, ANCHO_PANTALLA - ancho_asteroide)
    y = -alto_asteroide
    velocidad = random.randint(2, 6)
    
    return {
        'rect': pygame.Rect(x, y, ancho_asteroide, alto_asteroide),
        'velocidad': velocidad,
        'color': ROJO
    }

def mover_nave(nave_rect, teclas):

    velocidad_nave = 5
    
    if teclas[pygame.K_LEFT] and nave_rect.left > 0:
        nave_rect.x -= velocidad_nave
    if teclas[pygame.K_RIGHT] and nave_rect.right < ANCHO_PANTALLA:
        nave_rect.x += velocidad_nave

def actualizar_asteroides(lista_asteroides):

    asteroides_activos = []
    
    for asteroide in lista_asteroides:
        asteroide['rect'].y += asteroide['velocidad']
        
        if asteroide['rect'].top < ALTO_PANTALLA:
            asteroides_activos.append(asteroide)
    
    return asteroides_activos

def dibujar_asteroides(pantalla, lista_asteroides):

    for asteroide in lista_asteroides:
        pygame.draw.rect(pantalla, asteroide['color'], asteroide['rect'])

def mostrar_puntuacion(pantalla, puntuacion):

    dibujar_texto_centrado(pantalla, f"Puntuación: {puntuacion}", 36, BLANCO, 10)

def crear_nave_inicial():

    ancho_nave = 50
    alto_nave = 30
    x = ANCHO_PANTALLA // 2 - ancho_nave // 2
    y = ALTO_PANTALLA - alto_nave - 20
    
    return pygame.Rect(x, y, ancho_nave, alto_nave)

def generar_asteroide_tiempo(tiempo_ultimo_asteroide, tiempo_actual):

    intervalo_asteroides = 2000 
    return tiempo_actual - tiempo_ultimo_asteroide >= intervalo_asteroides

def dibujar_fondo_espacial(pantalla):

    pantalla.fill(NEGRO)
    
    for i in range(20):
        x = random.randint(0, ANCHO_PANTALLA)
        y = random.randint(0, ALTO_PANTALLA)
        pygame.draw.circle(pantalla, BLANCO, (x, y), 1)

def obtener_rectangulo_centrado(ancho, alto, x_centro, y_centro):

    x = x_centro - ancho // 2
    y = y_centro - alto // 2
    return pygame.Rect(x, y, ancho, alto)