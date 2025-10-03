"""
Clase Nave para el juego Asteroides Espaciales
Representa la nave espacial controlada por el jugador
"""

import pygame
from .utils import ANCHO_PANTALLA, ALTO_PANTALLA, VERDE, AZUL

class Nave:
    """
    Clase que representa la nave espacial del jugador
    Encapsula todas las propiedades y comportamientos de la nave
    """
    
    def __init__(self, x=None, y=None):
        """
        Constructor de la clase Nave
        Inicializa la nave con posición y propiedades por defecto
        Parámetros:
        - x: Posición horizontal (opcional, se centra si no se especifica)
        - y: Posición vertical (opcional, se posiciona abajo si no se especifica)
        """
        # Dimensiones de la nave
        self.ancho = 50
        self.alto = 30
        
        # Posición inicial (centrada horizontalmente, abajo de la pantalla)
        if x is None:
            x = ANCHO_PANTALLA // 2 - self.ancho // 2
        if y is None:
            y = ALTO_PANTALLA - self.alto - 20
            
        # Rectángulo de la nave (usado para colisiones y dibujo)
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        
        # Propiedades de movimiento
        self.velocidad = 5
        self.vida = 100  # Sistema de vida (para futuras mejoras)
        
        # Estado de la nave
        self.activa = True
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        
        # Color de la nave
        self.color = VERDE
        self.color_invulnerable = AZUL
    
    def mover_izquierda(self):
        """
        Método para mover la nave hacia la izquierda
        Verifica que no salga de los límites de la pantalla
        """
        if self.rect.left > 0:
            self.rect.x -= self.velocidad
    
    def mover_derecha(self):
        """
        Método para mover la nave hacia la derecha
        Verifica que no salga de los límites de la pantalla
        """
        if self.rect.right < ANCHO_PANTALLA:
            self.rect.x += self.velocidad
    
    def mover_arriba(self):
        """
        Método para mover la nave hacia arriba
        Verifica que no salga de los límites de la pantalla
        """
        if self.rect.top > 0:
            self.rect.y -= self.velocidad
    
    def mover_abajo(self):
        """
        Método para mover la nave hacia abajo
        Verifica que no salga de los límites de la pantalla
        """
        if self.rect.bottom < ALTO_PANTALLA:
            self.rect.y += self.velocidad
    
    def actualizar(self, teclas_presionadas):
        """
        Método principal para actualizar el estado de la nave
        Parámetros:
        - teclas_presionadas: Diccionario con el estado de las teclas
        """
        # Verificar si la nave está activa
        if not self.activa:
            return
        
        # Manejar movimiento con flechas
        if teclas_presionadas[pygame.K_LEFT]:
            self.mover_izquierda()
        if teclas_presionadas[pygame.K_RIGHT]:
            self.mover_derecha()
        if teclas_presionadas[pygame.K_UP]:
            self.mover_arriba()
        if teclas_presionadas[pygame.K_DOWN]:
            self.mover_abajo()
        
        # Actualizar estado de invulnerabilidad
        if self.invulnerable:
            self.tiempo_invulnerable -= 1
            if self.tiempo_invulnerable <= 0:
                self.invulnerable = False
    
    def dibujar(self, pantalla):
        """
        Método para dibujar la nave en la pantalla
        Parámetros:
        - pantalla: Superficie de pygame donde dibujar
        """
        if not self.activa:
            return
        
        # Elegir color según el estado de invulnerabilidad
        color_actual = self.color_invulnerable if self.invulnerable else self.color
        
        # Dibujar el cuerpo principal de la nave
        pygame.draw.rect(pantalla, color_actual, self.rect)
        
        # Dibujar detalles de la nave (opcional)
        self._dibujar_detalles(pantalla)
    
    def _dibujar_detalles(self, pantalla):
        """
        Método privado para dibujar detalles adicionales de la nave
        Parámetros:
        - pantalla: Superficie de pygame donde dibujar
        """
        # Dibujar una pequeña cabina en la parte superior
        cabina_rect = pygame.Rect(
            self.rect.x + self.rect.width // 4,
            self.rect.y,
            self.rect.width // 2,
            self.rect.height // 3
        )
        pygame.draw.rect(pantalla, (200, 200, 200), cabina_rect)
    
    def recibir_dano(self, cantidad=10):
        """
        Método para que la nave reciba daño
        Parámetros:
        - cantidad: Cantidad de daño a recibir
        """
        if self.invulnerable:
            return
        
        self.vida -= cantidad
        if self.vida <= 0:
            self.activa = False
        else:
            # Activar invulnerabilidad temporal
            self.invulnerable = True
            self.tiempo_invulnerable = 60  # 1 segundo a 60 FPS
    
    def curar(self, cantidad=10):
        """
        Método para curar la nave
        Parámetros:
        - cantidad: Cantidad de vida a recuperar
        """
        self.vida = min(100, self.vida + cantidad)
    
    def reiniciar(self):
        """
        Método para reiniciar la nave a su estado inicial
        """
        self.rect.x = ANCHO_PANTALLA // 2 - self.ancho // 2
        self.rect.y = ALTO_PANTALLA - self.alto - 20
        self.vida = 100
        self.activa = True
        self.invulnerable = False
        self.tiempo_invulnerable = 0
    
    def obtener_centro(self):
        """
        Método para obtener el centro de la nave
        Retorna: Tupla (x, y) con las coordenadas del centro
        """
        return self.rect.center
    
    def esta_activa(self):
        """
        Método para verificar si la nave está activa
        Retorna: True si está activa, False si no
        """
        return self.activa
    
    def obtener_vida(self):
        """
        Método para obtener la vida actual de la nave
        Retorna: Valor de vida actual
        """
        return self.vida
    
    def obtener_rectangulo(self):
        """
        Método para obtener el rectángulo de colisión de la nave
        Retorna: Rectángulo de pygame
        """
        return self.rect
