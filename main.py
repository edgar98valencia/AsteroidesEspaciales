import pygame
import sys
import random
from game.utils import (
    crear_pantalla, FPS, NEGRO, BLANCO, VERDE, ROJO, 
    dibujar_fondo_espacial, mostrar_puntuacion, detectar_colision
)
from game.nave import Nave
from game.asteroide import Asteroide
from game.menu import MenuManager

class JuegoAsteroides:
    def __init__(self):
        pygame.init()
        self.pantalla = crear_pantalla()
        self.reloj = pygame.time.Clock()
        self.estado = "menu_principal"
        self.jugando = False
        self.puntuacion = 0
        self.nivel = 1
        self.nave = None
        self.asteroides = []
        self.menu_manager = MenuManager()
        self.tiempo_ultimo_asteroide = 0
        self.intervalo_asteroides = 3000 
        self.velocidad_base_asteroides = 3
        self.asteroides_por_nivel = 5
        
    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.estado == "menu_principal":
                    self._manejar_menu_principal(evento)
                elif self.estado == "instrucciones":
                    self._manejar_instrucciones(evento)
                elif self.estado == "jugando":
                    self._manejar_juego(evento)
                elif self.estado == "pausa":
                    self._manejar_pausa(evento)
                elif self.estado == "game_over":
                    self._manejar_game_over(evento)
            if self.estado == "menu_principal":
                self._actualizar_menu_principal()
            elif self.estado == "instrucciones":
                self._actualizar_instrucciones()
            elif self.estado == "jugando":
                self._actualizar_juego()
            elif self.estado == "pausa":
                self._actualizar_pausa()
            elif self.estado == "game_over":
                self._actualizar_game_over()
            self.reloj.tick(FPS)
    
    def _manejar_menu_principal(self, evento):
        accion = self.menu_manager.manejar_eventos_menu(evento)
        if accion == "iniciar_juego":
            self._iniciar_juego()
        elif accion == "mostrar_instrucciones":
            self.estado = "instrucciones"
        elif accion == "salir":
            pygame.quit()
            sys.exit()
    
    def _manejar_instrucciones(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.estado = "menu_principal"
    
    def _manejar_juego(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = "pausa"
            elif evento.key == pygame.K_r:
                self._reiniciar_juego()
    
    def _manejar_pausa(self, evento):
        accion = self.menu_manager.manejar_eventos_menu(evento)
        if accion == "continuar_juego":
            self.estado = "jugando"
        elif accion == "reiniciar_juego":
            self._reiniciar_juego()
        elif accion == "volver_menu":
            self.estado = "menu_principal"
    
    def _manejar_game_over(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                self._reiniciar_juego()
            elif evento.key == pygame.K_ESCAPE:
                self.estado = "menu_principal"
    
    def _actualizar_menu_principal(self):
        self.menu_manager.mostrar_menu_principal(self.pantalla)
        pygame.display.flip()
    
    def _actualizar_instrucciones(self):
        self.menu_manager.mostrar_instrucciones(self.pantalla)
        pygame.display.flip()
    
    def _actualizar_juego(self):
        if not self.jugando:
            return
        teclas = pygame.key.get_pressed()
        self.nave.actualizar(teclas)
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_asteroide >= self.intervalo_asteroides:
            self._generar_asteroide()
            self.tiempo_ultimo_asteroide = tiempo_actual
        asteroides_activos = []
        for asteroide in self.asteroides:
            asteroide.actualizar()
            if asteroide.esta_activo():
                asteroides_activos.append(asteroide)
            else:
                self.puntuacion += asteroide.obtener_puntos()
        self.asteroides = asteroides_activos
        if self._verificar_colisiones():
            self.estado = "game_over"
            self.jugando = False
        self._actualizar_nivel()
        self._dibujar_juego()
    
    def _actualizar_pausa(self):
        self._dibujar_juego()
        self.menu_manager.mostrar_pausa(self.pantalla)
        pygame.display.flip()
    
    def _actualizar_game_over(self):
        self.menu_manager.mostrar_game_over(self.pantalla, self.puntuacion)
        pygame.display.flip()
    
    def _iniciar_juego(self):
        self.nave = Nave()
        self.asteroides = []
        self.puntuacion = 0
        self.nivel = 1
        self.jugando = True
        self.estado = "jugando"
        self.tiempo_ultimo_asteroide = pygame.time.get_ticks()
    
    def _reiniciar_juego(self):
        self._iniciar_juego()
    
    def _generar_asteroide(self):
        asteroide = Asteroide()
        velocidad_extra = (self.nivel - 1) * 0.5
        asteroide.cambiar_velocidad(asteroide.velocidad_y + velocidad_extra)
        self.asteroides.append(asteroide)
    
    def _verificar_colisiones(self):
        for asteroide in self.asteroides:
            if asteroide.colisionar_con(self.nave.obtener_rectangulo()):
                return True
        return False
    
    def _actualizar_nivel(self):
        nuevo_nivel = (self.puntuacion // 50) + 1
        if nuevo_nivel > self.nivel:
            self.nivel = nuevo_nivel
            self.intervalo_asteroides = max(1000, 2000 - (self.nivel * 200))
    
    def _dibujar_juego(self):
        dibujar_fondo_espacial(self.pantalla)
        if self.nave:
            self.nave.dibujar(self.pantalla)
        for asteroide in self.asteroides:
            asteroide.dibujar(self.pantalla)
        mostrar_puntuacion(self.pantalla, self.puntuacion)
        from game.utils import dibujar_texto_centrado
        dibujar_texto_centrado(self.pantalla, f"Nivel: {self.nivel}", 24, BLANCO, 50)
        dibujar_texto_centrado(self.pantalla, "ESC - Pausa | R - Reiniciar", 18, BLANCO, 570)
        pygame.display.flip()

def main():
    try:
        juego = JuegoAsteroides()
        juego.ejecutar()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
    except Exception as e:
        print(f"Error en el juego: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
