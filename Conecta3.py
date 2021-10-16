import numpy as np
import random
import pygame
import sys
import math

# Configuracion de juego
FILAS = 6
COLUMNAS = 7
#FILAS = 3
#COLUMNAS = 3
JUGADOR = 0
PC = 1

# Configuracion graficos
TAMANO_CUADRADO = 100
ANCHO_TABLERO = COLUMNAS * TAMANO_CUADRADO
ALTURA_TABLERO = (FILAS + 1) * TAMANO_CUADRADO
TAMANO_TABLERO = (ANCHO_TABLERO, ALTURA_TABLERO)
RADIO_CIRCULO = int(TAMANO_CUADRADO / 2 - 6)

# Colores juego
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Colores fichas
COLOR_JUGADOR = ROJO
COLOR_PC = AMARILLO

# Funciones auxiliares
def crearTablero():
    tablero = np.zeros((FILAS, COLUMNAS))
    return tablero

def imprimirTablero(tablero):
    print(np.flip(tablero, 0))

def ponerFicha(tablero, fila, columna, ficha):
   tablero[fila][columna] = ficha

def esPosicionValida(tablero, columna):
    return tablero[FILAS - 1][columna] == 0 # Hardcode, checa última

def obtenerSiguienteFila(tablero, columna):
    for fila in range(FILAS):
        if tablero[fila][columna] == 0:
            return fila

            
# Adaptado a Conecta 3
def movimientoGanador(tablero, ficha):
    # Checar posiciones horizontales
    for columna in range(COLUMNAS - 2): # Resta para no checar últimas posiciones, no se puede ganar ahí
        for fila in range(FILAS):
            if tablero[fila][columna] == ficha and tablero[fila][columna + 1] == ficha and tablero[fila][columna + 2] == ficha:
                return True

    # Checar posiciones verticales
    for columna in range(COLUMNAS):
        for fila in range(FILAS - 2):
            if tablero[fila][columna] == ficha and tablero[fila + 1][columna] == ficha and tablero[fila + 2][columna] == ficha:
                return True

    # Checar diagonales izq-der
    for columna in range(COLUMNAS - 2): # Resta para no checar últimas posiciones, no se puede ganar ahí
        for fila in range(FILAS - 2):
            if tablero[fila][columna] == ficha and tablero[fila + 1][columna + 1] == ficha and tablero[fila + 2][columna + 2] == ficha:
                return True

    # Checar diagonales der-izq
    for columna in range(COLUMNAS - 2): # Resta para no checar últimas posiciones, no se puede ganar ahí
        for fila in range(2, FILAS):
            if tablero[fila][columna] == ficha and tablero[fila - 1][columna + 1] == ficha and tablero[fila - 2][columna + 2] == ficha:
                return True

def primerTurno():
    return random.randint(JUGADOR, PC)

# Graficos
def dibujarTablero(tablero):
    for columna in range(COLUMNAS):
        for fila in range(FILAS):
            # Tablero
            pygame.draw.rect(pantalla, AZUL, (columna * TAMANO_CUADRADO, fila * TAMANO_CUADRADO + TAMANO_CUADRADO, TAMANO_CUADRADO, TAMANO_CUADRADO))
            # Fichas vacías
            pygame.draw.circle(pantalla, NEGRO, (int(columna * TAMANO_CUADRADO + TAMANO_CUADRADO / 2), int(fila * TAMANO_CUADRADO + TAMANO_CUADRADO + TAMANO_CUADRADO / 2)), RADIO_CIRCULO)

    # Fichas de jugadores
    for columna in range(COLUMNAS):
        for fila in range(FILAS):
            pos = tablero[fila][columna]
            if pos == 1:
                # Fichas Jugador
                pygame.draw.circle(pantalla, COLOR_JUGADOR, (int(columna * TAMANO_CUADRADO + TAMANO_CUADRADO / 2), ALTURA_TABLERO - int(fila * TAMANO_CUADRADO + TAMANO_CUADRADO / 2)), RADIO_CIRCULO)
            elif pos == 2:
                # Fichas PC
                pygame.draw.circle(pantalla, COLOR_PC, (int(columna * TAMANO_CUADRADO + TAMANO_CUADRADO / 2), ALTURA_TABLERO - int(fila * TAMANO_CUADRADO + TAMANO_CUADRADO / 2)), RADIO_CIRCULO)
                
    pygame.display.update()      

def mostrarGanador(ficha):
    # Volver a pintar rectangulo negro antes de mostrar mensaje
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO_TABLERO, TAMANO_CUADRADO)) 
    if ficha == 1: 
        font = pygame.font.SysFont("monospace", 50)
        label = font.render("¡Gana el Jugador!", 1, COLOR_JUGADOR)
        pantalla.blit(label, (100, 25))
    elif ficha == 2:
        font = pygame.font.SysFont("monospace", 50)
        label = font.render("Gana la PC", 1, COLOR_PC)
        pantalla.blit(label, (195, 25))


# Jugar
def jugarJuego():
    gameOver = False
    turno = primerTurno()

    while not gameOver:
        for event in pygame.event.get():
            # Salir del juego
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                # Volver a pintar rectangulo negro antes de pintar la ficha actual
                pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO_TABLERO, TAMANO_CUADRADO)) 
                pos_x = event.pos[0]
                if turno == JUGADOR:
                    pygame.draw.circle(pantalla, COLOR_JUGADOR, (pos_x, int(TAMANO_CUADRADO / 2)), RADIO_CIRCULO)
            pygame.display.update()

            # Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Turno del Jugador (1)
                if turno == JUGADOR:
                    pos_x = event.pos[0]
                    columna = int(math.floor(pos_x / TAMANO_CUADRADO))
                    
                    if esPosicionValida(tablero, columna):
                        fila = obtenerSiguienteFila(tablero, columna)
                        ponerFicha(tablero, fila, columna, 1) 

                        if movimientoGanador(tablero, 1):
                            print("¡Gana el Jugador!")
                            mostrarGanador(1)
                            gameOver = True

                         # Continuar juego
                        turno = (turno + 1) % 2
                        imprimirTablero(tablero)
                        dibujarTablero(tablero)

        # Turno de la PC (2)
        if turno == PC and not gameOver:
            columna = random.randint(0, COLUMNAS - 1)
            
            if esPosicionValida(tablero, columna):
                pygame.time.wait(500)
                fila = obtenerSiguienteFila(tablero, columna)
                ponerFicha(tablero, fila, columna, 2) 

                if movimientoGanador(tablero, 2):
                    print("Gana la PC")
                    mostrarGanador(2)
                    gameOver = True

                # Continuar juego
                turno = (turno + 1) % 2
                imprimirTablero(tablero)
                dibujarTablero(tablero)

        # Se termina el juego
        if gameOver:
            pygame.time.wait(3000)



# Iniciar juego
if __name__ == '__main__':
    tablero = crearTablero()
    imprimirTablero(tablero)

    # Graficos
    pantalla = pygame.display.set_mode(TAMANO_TABLERO)

    # Poner fondo blanco
    # pantalla.fill(BLANCO)

    dibujarTablero(tablero)
    pygame.init()
    jugarJuego()



    



    

