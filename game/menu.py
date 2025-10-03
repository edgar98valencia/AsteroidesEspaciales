import pygame
from .utils import (
    ANCHO_PANTALLA, ALTO_PANTALLA, NEGRO, BLANCO, VERDE, 
    ROJO, AZUL, AMARILLO, dibujar_texto_centrado, 
    dibujar_texto_centrado_completo, obtener_rectangulo_centrado
)

class MenuManager:
    
    def __init__(self):

        self.estado_actual = "principal"
        self.opcion_seleccionada = 0
        self.max_opciones = 3
        
        self.color_titulo = AMARILLO
        self.color_opcion_seleccionada = VERDE
        self.color_opcion_normal = BLANCO
        self.color_instrucciones = AZUL
        
        self.parpadeo_titulo = 0
        self.velocidad_parpadeo = 5
    
    def mostrar_menu_principal(self, pantalla):

        pantalla.fill(NEGRO)
        
        self.parpadeo_titulo += self.velocidad_parpadeo
        if self.parpadeo_titulo > 255:
            self.parpadeo_titulo = 0
        
        color_titulo_actual = (self.color_titulo[0], self.color_titulo[1], self.color_titulo[2])
        dibujar_texto_centrado(pantalla, "ASTEROIDES ESPACIALES", 72, color_titulo_actual, 100)
        
        dibujar_texto_centrado(pantalla, "Un juego de supervivencia espacial", 36, BLANCO, 180)
        
        opciones = [
            "INICIAR JUEGO",
            "INSTRUCCIONES", 
            "SALIR"
        ]
        
        y_inicio = 280
        for i, opcion in enumerate(opciones):
            color = self.color_opcion_seleccionada if i == self.opcion_seleccionada else self.color_opcion_normal
            dibujar_texto_centrado(pantalla, opcion, 48, color, y_inicio + i * 60)
        
        dibujar_texto_centrado(pantalla, "Usa las flechas ↑↓ para navegar", 24, self.color_instrucciones, 500)
        dibujar_texto_centrado(pantalla, "Presiona ENTER para seleccionar", 24, self.color_instrucciones, 530)
        
        return "principal"
    
    def mostrar_instrucciones(self, pantalla):

        pantalla.fill(NEGRO)
        
        # Título
        dibujar_texto_centrado(pantalla, "INSTRUCCIONES", 64, AMARILLO, 50)
        
        instrucciones = [
            "OBJETIVO:",
            "Evita los asteroides que caen desde arriba",
            "",
            "CONTROLES:",
            "↑ Flecha Arriba - Mover nave hacia arriba",
            "↓ Flecha Abajo - Mover nave hacia abajo", 
            "← Flecha Izquierda - Mover nave hacia la izquierda",
            "→ Flecha Derecha - Mover nave hacia la derecha",
            "",
            "REGLAS:",
            "• Los asteroides rojos son más peligrosos",
            "• Los asteroides amarillos son menos peligrosos",
            "• Evita cualquier colisión para sobrevivir",
            "• Gana puntos por cada asteroide que evites"
        ]
        
        y_pos = 120
        for instruccion in instrucciones:
            if instruccion.startswith(("OBJETIVO:", "CONTROLES:", "REGLAS:")):
                color = AMARILLO
                tamaño = 32
            elif instruccion.startswith(("•")):
                color = VERDE
                tamaño = 24
            else:
                color = BLANCO
                tamaño = 24
            
            dibujar_texto_centrado(pantalla, instruccion, tamaño, color, y_pos)
            y_pos += 30
        
        # Botón para volver
        dibujar_texto_centrado(pantalla, "Presiona ESC para volver al menú", 28, AZUL, 550)
        
        return "instrucciones"
    
    def mostrar_game_over(self, pantalla, puntuacion_final):

        pantalla.fill(NEGRO)
        
        dibujar_texto_centrado(pantalla, "GAME OVER", 72, ROJO, 150)
        
        dibujar_texto_centrado(pantalla, f"Puntuación Final: {puntuacion_final}", 48, BLANCO, 250)
        
        if puntuacion_final >= 100:
            mensaje = "¡EXCELENTE TRABAJO!"
            color_mensaje = AMARILLO
        elif puntuacion_final >= 50:
            mensaje = "¡BUEN TRABAJO!"
            color_mensaje = VERDE
        else:
            mensaje = "¡SIGUE INTENTANDO!"
            color_mensaje = AZUL
        
        dibujar_texto_centrado(pantalla, mensaje, 36, color_mensaje, 320)
        
        dibujar_texto_centrado(pantalla, "Presiona R para REINICIAR", 32, VERDE, 400)
        dibujar_texto_centrado(pantalla, "Presiona ESC para SALIR", 32, ROJO, 440)
        
        return "game_over"
    
    def mostrar_pausa(self, pantalla):
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        overlay.set_alpha(128)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        dibujar_texto_centrado(pantalla, "PAUSA", 64, AMARILLO, 200)
        
        opciones_pausa = [
            "CONTINUAR JUEGO",
            "REINICIAR",
            "VOLVER AL MENÚ"
        ]
        
        y_inicio = 280
        for i, opcion in enumerate(opciones_pausa):
            color = self.color_opcion_seleccionada if i == self.opcion_seleccionada else self.color_opcion_normal
            dibujar_texto_centrado(pantalla, opcion, 36, color, y_inicio + i * 50)
        
        dibujar_texto_centrado(pantalla, "Usa ↑↓ para navegar, ENTER para seleccionar", 24, BLANCO, 450)
        
        return "pausa"
    
    def manejar_eventos_menu(self, evento):

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % self.max_opciones
            elif evento.key == pygame.K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % self.max_opciones
            elif evento.key == pygame.K_RETURN:
                return self._procesar_seleccion()
            elif evento.key == pygame.K_ESCAPE:
                return "salir"
        
        return None
    
    def _procesar_seleccion(self):
   
        if self.estado_actual == "principal":
            if self.opcion_seleccionada == 0:
                return "iniciar_juego"
            elif self.opcion_seleccionada == 1:
                return "mostrar_instrucciones"
            elif self.opcion_seleccionada == 2:
                return "salir"
        
        elif self.estado_actual == "pausa":
            if self.opcion_seleccionada == 0:
                return "continuar_juego"
            elif self.opcion_seleccionada == 1:
                return "reiniciar_juego"
            elif self.opcion_seleccionada == 2:
                return "volver_menu"
        
        return None
    
    def cambiar_estado(self, nuevo_estado):

        self.estado_actual = nuevo_estado
        self.opcion_seleccionada = 0
    
    def obtener_estado(self):
     
        return self.estado_actual