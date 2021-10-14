import numpy as np

# Variables de juego
gameOver = False
turno = 0
FILAS = 6
COLUMNAS = 7

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

# Iniciar juego
if __name__ == '__main__':
    tablero = crearTablero()
    imprimirTablero(tablero)

while not gameOver:
    # Preguntar por Jugador (1)
    if turno % 2 == 0:
        columna = int(input(f'Turno del Jugador (1-{COLUMNAS - 1}):')) - 1
        if esPosicionValida(tablero, columna):
            fila = obtenerSiguienteFila(tablero, columna)
            ponerFicha(tablero, fila, columna, 1) 

            if movimientoGanador(tablero, 1):
                print("¡Gana el Jugador!")
                gameOver = True
                break

    # Preguntar por PC (2)
    else:
        columna = int(input(f'Turno de la PC (1-{COLUMNAS - 1}):')) - 1
        if esPosicionValida(tablero, columna):
            fila = obtenerSiguienteFila(tablero, columna)
            ponerFicha(tablero, fila, columna, 2) 

            if movimientoGanador(tablero, 2):
                print("Gana la PC")
                gameOver = True
                break

    # Continuar juego
    turno += 1
    imprimirTablero(tablero)

