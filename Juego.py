import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Definir constantes
ANCHO = 400
ALTO = 550  # Incrementamos la altura para dar espacio al mensaje, al menú y al número de aprendizajes
TAM_CASILLA = 100
MENSAJE_ALTO = 50  # Altura del mensaje
MENÚ_ALTO = 50  # Altura del menú
MENÚ_COLOR = (200, 200, 200)

# Inicializar la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Totito")

# Variables para el número de aprendizajes
aprendizajes = 0

# Definir la profundidad del algoritmo minimax
PROFUNDIDAD_MINIMAX = 4

class Nodo:
    def __init__(self, tablero, jugador, valor):
        self.tablero = tablero  # Configuración del tablero en este nodo
        self.jugador = jugador  # Jugador que realizó el movimiento
        self.valor = valor      # Valor asignado a este nodo
        self.hijos = []         # Lista de hijos (nodos) generados a partir de este nodo

def dibujar_tablero(tablero, ganador, victorias_jugador1, victorias_jugador2):
    ventana.fill(BLANCO)

    # Dibujar mensaje
    fuente_mensaje = pygame.font.SysFont(None, 20)
    mensaje_renderizado = fuente_mensaje.render("Leonardo José Valdéz Flores 9490-22-5890", True, NEGRO)
    ventana.blit(mensaje_renderizado, (ANCHO // 2 - mensaje_renderizado.get_width() // 2, 10))

    # Dibujar el tablero
    for x in range(3):
        for y in range(3):
            pygame.draw.rect(ventana, NEGRO, (x * TAM_CASILLA, MENSAJE_ALTO + y * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA), 3)

    # Dibujar las fichas en el tablero
    for fila in range(3):
        for columna in range(3):
            jugador = tablero[fila][columna]
            if jugador != 0:
                texto = "X" if jugador == 1 else "O"
                fuente = pygame.font.SysFont(None, 100)
                texto_renderizado = fuente.render(texto, True, AZUL)
                ventana.blit(texto_renderizado, (columna * TAM_CASILLA + TAM_CASILLA // 2 - texto_renderizado.get_width() // 2, MENSAJE_ALTO + fila * TAM_CASILLA + TAM_CASILLA // 2 - texto_renderizado.get_height() // 2))

    # Dibujar el menú
    pygame.draw.rect(ventana, MENÚ_COLOR, (0, ALTO - MENÚ_ALTO - 50, ANCHO, MENÚ_ALTO))

    if ganador != 0:
        fuente = pygame.font.SysFont(None, 30)
        texto_renderizado = fuente.render(f"Jugador 1: {victorias_jugador1}", True, NEGRO)
        ventana.blit(texto_renderizado, (ANCHO // 4 - texto_renderizado.get_width() // 2, ALTO - MENÚ_ALTO + -90))
        texto_renderizado = fuente.render(f"Jugador 2: {victorias_jugador2}", True, NEGRO)
        ventana.blit(texto_renderizado, (3 * ANCHO // 4 - texto_renderizado.get_width() // 2, ALTO - MENÚ_ALTO - 90))
        texto_renderizado = fuente.render("Reintentar", True, NEGRO)
        ventana.blit(texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO - MENÚ_ALTO - 30))
    else:
        fuente = pygame.font.SysFont(None, 30)
        texto_renderizado = fuente.render("Reintentar", True, NEGRO)
        ventana.blit(texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO - MENÚ_ALTO - 30))

    # Dibujar número de aprendizajes
    texto_aprendizajes = f"Aprendizajes: {aprendizajes}"
    texto_renderizado = fuente.render(texto_aprendizajes, True, NEGRO)
    ventana.blit(texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO - MENÚ_ALTO))

    pygame.display.update()

def verificar_ganador(tablero):
    for fila in tablero:
        if fila[0] == fila[1] == fila[2] != 0:
            return fila[0]

    for columna in range(3):
        if tablero[0][columna] == tablero[1][columna] == tablero[2][columna] != 0:
            return tablero[0][columna]

    if tablero[0][0] == tablero[1][1] == tablero[2][2] != 0:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != 0:
        return tablero[0][2]

    return 0

def generar_movimientos(tablero, jugador):
    movimientos = []

    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == 0:
                nuevo_tablero = [fila[:] for fila in tablero]  # Copiar el tablero actual
                nuevo_tablero[fila][columna] = jugador
                movimientos.append(nuevo_tablero)

    return movimientos

def calcular_valor_tablero(tablero, jugador):
    ganador = verificar_ganador(tablero)
    if ganador == jugador:
        return 1  # Victoria del jugador
    elif ganador == 2 if jugador == 1 else 1:
        return -1  # Derrota del jugador
    else:
        return 0  # Empate o juego en curso

def construir_arbol(tablero, jugador, profundidad):
    nodo = Nodo(tablero, jugador, 0)

    if profundidad == 0 or verificar_ganador(tablero) != 0:
        nodo.valor = calcular_valor_tablero(tablero, jugador)
        return nodo

    movimientos = generar_movimientos(tablero, jugador)
    for movimiento in movimientos:
        nuevo_jugador = 2 if jugador == 1 else 1
        nodo.hijos.append(construir_arbol(movimiento, nuevo_jugador, profundidad - 1))

    return nodo

def minimax(nodo, profundidad, jugador_maximizante):
    if profundidad == 0 or verificar_ganador(nodo.tablero) != 0:
        return nodo.valor

    if jugador_maximizante:
        mejor_valor = float('-inf')
        for hijo in nodo.hijos:
            valor = minimax(hijo, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        nodo.valor = mejor_valor
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for hijo in nodo.hijos:
            valor = minimax(hijo, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        nodo.valor = mejor_valor
        return mejor_valor

def obtener_mejor_movimiento(tablero, jugador):
    raiz = construir_arbol(tablero, jugador, PROFUNDIDAD_MINIMAX)
    mejor_valor = float('-inf')
    mejor_movimiento = None

    for hijo in raiz.hijos:
        valor = minimax(hijo, PROFUNDIDAD_MINIMAX, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = hijo.tablero

    if mejor_movimiento is None:  # Si no se encuentra un mejor movimiento, devolver el tablero actual
        return tablero

    return mejor_movimiento

def main():
    global aprendizajes
    jugador = 1
    tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    victorias_jugador1 = 0
    victorias_jugador2 = 0
    while True:
        ganador = verificar_ganador(tablero)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and ganador == 0 and jugador == 1:
                pos = pygame.mouse.get_pos()
                fila = (pos[1] - MENSAJE_ALTO) // TAM_CASILLA
                columna = pos[0] // TAM_CASILLA
                if fila >= 0 and fila < 3 and columna >= 0 and columna < 3 and tablero[fila][columna] == 0:
                    tablero[fila][columna] = jugador
                    jugador = 2  # Cambio de turno al jugador 2 (computadora)
                    aprendizajes += 1  # Se incrementa el contador de aprendizajes

                    # Movimiento del jugador 2 (computadora) inmediatamente después del jugador 1
                    if verificar_ganador(tablero) == 0:  # Verificar si el juego continúa
                        tablero = obtener_mejor_movimiento(tablero, jugador)
                        jugador = 1  # Cambio de turno al jugador 1 (humano)

            elif evento.type == pygame.MOUSEBUTTONDOWN and ganador != 0:
                tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                jugador = 1
                if ganador == 1:
                    victorias_jugador1 += 1
                elif ganador == 2:
                    victorias_jugador2 += 1

        dibujar_tablero(tablero, ganador, victorias_jugador1, victorias_jugador2)

if __name__ == "__main__":
    main()