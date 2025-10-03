
import pygame
import random
from .utils import ANCHO_PANTALLA, ALTO_PANTALLA, ROJO, NARANJA, AMARILLO

class Asteroide:
    
    def __init__(self, x=None, y=None, tamaño=None):
   
        if tamaño is None:
            self.tamaño = random.randint(20, 60)
        else:
            self.tamaño = tamaño
            
        if x is None:
            x = random.randint(0, ANCHO_PANTALLA - self.tamaño)
        if y is None:
            y = -self.tamaño 
            
        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        
        self.velocidad_y = random.randint(1, 4)
        self.velocidad_x = random.randint(-2, 2)  
        
        self.activo = True
        self.daño = 10
        self.puntos = 5
        
        self._asignar_color()
        
        self.rotacion = 0
        self.velocidad_rotacion = random.randint(1, 5)
    
    def _asignar_color(self):

        if self.tamaño >= 50:
            self.color = ROJO 
        elif self.tamaño >= 35:
            self.color = NARANJA
        else:
            self.color = AMARILLO
    
    def actualizar(self):

        if not self.activo:
            return
        
        self.rect.y += self.velocidad_y
        
        self.rect.x += self.velocidad_x
        
        if self.rect.top > ALTO_PANTALLA:
            self.activo = False
        
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x = -self.velocidad_x 
        
        self.rotacion += self.velocidad_rotacion
        if self.rotacion >= 360:
            self.rotacion = 0
    
    def dibujar(self, pantalla):

        if not self.activo:
            return
        
        pygame.draw.rect(pantalla, self.color, self.rect)
        
        self._dibujar_detalles(pantalla)
    
    def _dibujar_detalles(self, pantalla):
  
        pygame.draw.rect(pantalla, (100, 0, 0), self.rect, 2)
        
        centro_x = self.rect.centerx
        centro_y = self.rect.centery
        
        pygame.draw.line(pantalla, (150, 0, 0), 
                        (self.rect.left, self.rect.top), 
                        (self.rect.right, self.rect.bottom), 1)
        pygame.draw.line(pantalla, (150, 0, 0), 
                        (self.rect.right, self.rect.top), 
                        (self.rect.left, self.rect.bottom), 1)
    
    def colisionar_con(self, otro_rectangulo):

        if not self.activo:
            return False
        
        return self.rect.colliderect(otro_rectangulo)
    
    def destruir(self):

        self.activo = False
    
    def obtener_puntos(self):

        return self.puntos
    
    def obtener_daño(self):

        return self.daño
    
    def esta_activo(self):
 
        return self.activo
    
    def obtener_rectangulo(self):

        return self.rect
    
    def cambiar_velocidad(self, nueva_velocidad):

        self.velocidad_y = nueva_velocidad
    
    def acelerar(self, incremento):

        self.velocidad_y += incremento
    
    def obtener_tamaño(self):
   
        return self.tamaño
    
    def obtener_posicion(self):

        return (self.rect.x, self.rect.y)