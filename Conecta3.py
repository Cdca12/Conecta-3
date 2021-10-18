import numpy as np
import random
import pygame
import sys
import math

# Configuracion de juego
FILAS = 3
COLUMNAS = 3
CONECTA_FICHAS = 3
DIFICULTAD = 3

JUGADOR = 0
PC = 1

FICHA_VACIA = 0
FICHA_JUGADOR = 1
FICHA_PC = 2

LONGITUD_VENTANA = 3

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
    return tablero[FILAS - 1][columna] == FICHA_VACIA

def obtenerSiguienteFila(tablero, columna):
    for fila in range(FILAS):
        if tablero[fila][columna] == FICHA_VACIA:
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
            if pos == FICHA_JUGADOR:
                pygame.draw.circle(pantalla, COLOR_JUGADOR, (int(columna * TAMANO_CUADRADO + TAMANO_CUADRADO / 2), ALTURA_TABLERO - int(fila * TAMANO_CUADRADO + TAMANO_CUADRADO / 2)), RADIO_CIRCULO)
            elif pos == FICHA_PC:
                pygame.draw.circle(pantalla, COLOR_PC, (int(columna * TAMANO_CUADRADO + TAMANO_CUADRADO / 2), ALTURA_TABLERO - int(fila * TAMANO_CUADRADO + TAMANO_CUADRADO / 2)), RADIO_CIRCULO)
                
    pygame.display.update()      

def mostrarGanador(ficha):
    # Volver a pintar rectangulo negro antes de mostrar mensaje
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO_TABLERO, TAMANO_CUADRADO)) 
    if ficha == FICHA_JUGADOR: 
        font = pygame.font.SysFont("monospace", 25)
        label = font.render("¡Gana el Jugador!", 1, COLOR_JUGADOR)
        pantalla.blit(label, (25, 30))
    elif ficha == FICHA_PC:
        font = pygame.font.SysFont("monospace", 40)
        label = font.render("Gana la PC", 1, COLOR_PC)
        pantalla.blit(label, (30, 25))

# Inteligencia Artificial

def evaluarVentana(ventana, ficha):
    puntuacion = 0

    # Alternar turno
    fichaContraria = FICHA_PC if ficha == FICHA_JUGADOR else FICHA_JUGADOR

    # Gana juego
    if ventana.count(ficha) == CONECTA_FICHAS:
        puntuacion += 100
    # Conecta 2
    elif ventana.count(ficha) == (CONECTA_FICHAS - 1) and ventana.count(FICHA_VACIA) == 1:
        puntuacion += 5
    # Fichas contrincante
    if ventana.count(fichaContraria) == (CONECTA_FICHAS - 1) and ventana.count(FICHA_VACIA) == 1:
        puntuacion -= 4

    return puntuacion

def calcularPuntuacionTablero(tablero, ficha):
    puntuacion = 0

    # Puntuacion columna central
    arregloCentral = [int(i) for i in list(tablero[:, COLUMNAS // 2])]
    contadorCentral = arregloCentral.count(ficha)
    puntuacion += contadorCentral * 3

    # Puntuacion horizontal
    for fila in range(FILAS):
        arregloFilas = [int(i) for i in list(tablero[fila, :])]
        for columna in range(COLUMNAS - 2):
            ventana = arregloFilas[columna:columna + LONGITUD_VENTANA]
            puntuacion += evaluarVentana(ventana, ficha)

    # Puntuacion vertical
    for columna in range(COLUMNAS):
        arregloColumnas = [int(i) for i in list(tablero[:, columna])]
        for fila in range(FILAS - 2):
            ventana = arregloColumnas[fila:fila + LONGITUD_VENTANA]
            puntuacion += evaluarVentana(ventana, ficha)

    # Checar diagonales
    for fila in range(FILAS - 2):
        for columna in range(COLUMNAS - 2):
            ventana = [tablero[fila + i][columna + i] for i in range(LONGITUD_VENTANA)]
            puntuacion += evaluarVentana(ventana, ficha)

    for fila in range(FILAS - 2):
        for columna in range(COLUMNAS - 2):
            ventana = [tablero[fila + 2 - i][columna + i] for i in range(LONGITUD_VENTANA)]
            puntuacion += evaluarVentana(ventana, ficha)

    return puntuacion

# Implementación de Algoritmo Mini-Max

## Nodo: En este caso, sería el tablero
## Nivel: Qué tan lejos vamos a buscar hacia abajo en nuestro juego
## maximizandoJugador: Será True para la PC y Falso cuando busquemos los movimientos del Jugador
## NodoTerminal: Es cuando un juego se gana (Jugador o PC) o se llega al final del juego
## - Aquí se regresará el valor heurístico de ese nodo, si no, revisamos recursivamente el arbol para encontrar la mejor puntuación

def esNodoTerminal(nodo):
    return movimientoGanador(nodo, FICHA_JUGADOR) or movimientoGanador(nodo, FICHA_PC) or len(obtenerPosicionesValidas(nodo)) == 0

def miniMax(nodo, nivel, maximizandoJugador):
    nodoTerminal = esNodoTerminal(nodo)
    tablero = nodo # Solo para darle más sentido semántico al código
    posicionesValidas = obtenerPosicionesValidas(tablero)
    # Caso base, obtenemos valor heurístico del nodo (tablero)
    if nivel == 0 or nodoTerminal:
        if nodoTerminal:
            if movimientoGanador(tablero, FICHA_PC):
                return (None, 10000000000000000) # Regresamos la mejor puntuación 
            elif movimientoGanador(tablero, FICHA_JUGADOR):
                return (None, -10000000000000000) # Regresamos la peor puntuación
            else: # Game Over, sin más movimientos válidos
                return (None, 0) 
        else: # nivel es 0
            return (None, calcularPuntuacionTablero(tablero, FICHA_PC))
    if maximizandoJugador: # Entra cuando es la PC
        valorActual = -math.inf
        mejorColumna = random.choice(posicionesValidas)
        for columna in posicionesValidas:
            fila = obtenerSiguienteFila(tablero, columna)
            tableroTemporal = tablero.copy()
            ponerFicha(tableroTemporal, fila, columna, FICHA_PC)
            nuevaPuntuacion = miniMax(tableroTemporal, nivel - 1, False)[1]
            # Obtener el maximo y guardar columna
            if nuevaPuntuacion > valorActual:
                valorActual = nuevaPuntuacion
                mejorColumna = columna
        return (mejorColumna, nuevaPuntuacion)
    else: # Minimizando jugador, entra cuando es el Jugador
        valorActual = math.inf
        mejorColumna = random.choice(posicionesValidas)
        for columna in posicionesValidas:
            fila = obtenerSiguienteFila(tablero, columna)
            tableroTemporal = tablero.copy()
            ponerFicha(tableroTemporal, fila, columna, FICHA_JUGADOR)
            nuevaPuntuacion = miniMax(tableroTemporal, nivel - 1, True)[1]
            # Obtener el minimo y guardar columna
            if nuevaPuntuacion < valorActual:
                valorActual = nuevaPuntuacion
                mejorColumna = columna
        return (mejorColumna, nuevaPuntuacion)


def obtenerPosicionesValidas(tablero):
    posicionesValidas = []
    for columna in range(COLUMNAS):
        if esPosicionValida(tablero, columna):
            posicionesValidas.append(columna)
    return posicionesValidas

# Inteligencia anterior, ya no se usa
def elegirMejorMovimiento(tablero, ficha):
    posicionesValidas = obtenerPosicionesValidas(tablero)
    mejorPuntuacion = -10000
    mejorColumna = random.choice(posicionesValidas)
    for columna in posicionesValidas:
        fila = obtenerSiguienteFila(tablero, ficha)
        tableroTemporal = tablero.copy()
        ponerFicha(tableroTemporal, fila, columna, ficha)
        puntuacion = calcularPuntuacionTablero(tableroTemporal, ficha)

        # Comparar puntuaciones, simple método de búsqueda secuencial
        if puntuacion > mejorPuntuacion: 
            mejorPuntuacion = puntuacion
            mejorColumna = columna

    return mejorColumna


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
                # Turno del Jugador
                if turno == JUGADOR:
                    pos_x = event.pos[0]
                    columna = int(math.floor(pos_x / TAMANO_CUADRADO))
                    
                    if esPosicionValida(tablero, columna):
                        fila = obtenerSiguienteFila(tablero, columna)
                        ponerFicha(tablero, fila, columna, FICHA_JUGADOR) 

                        if movimientoGanador(tablero, FICHA_JUGADOR):
                            print("¡Gana el Jugador!")
                            mostrarGanador(FICHA_JUGADOR)
                            gameOver = True

                         # Continuar juego
                        turno = (turno + 1) % 2
                        imprimirTablero(tablero)
                        dibujarTablero(tablero)

        # Turno de la PC
        if turno == PC and not gameOver:
            # columna = random.randint(0, COLUMNAS - 1) # Columna random, 0 logica
            # columna = elegirMejorMovimiento(tablero, FICHA_PC) # Inteligencia basica anterior
            columna, valorMiniMax = miniMax(tablero, DIFICULTAD, True) # True porque es turno de la PC
            
            if esPosicionValida(tablero, columna):
                pygame.time.wait(500)
                fila = obtenerSiguienteFila(tablero, columna)
                ponerFicha(tablero, fila, columna, FICHA_PC) 

                if movimientoGanador(tablero, FICHA_PC):
                    print("Gana la PC")
                    mostrarGanador(FICHA_PC)
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



    



    

