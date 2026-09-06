# =====================================================
# ENTRADA: solo arranca el juego (python main.py)
# =====================================================

import vista
import modelo
import controlador
import random

def main():
    # bucle de partidas: elegir pokemon, batallar, revancha
    vista.activar_colores()
    print("=== POKEMON 1vs1 ===")
    while True:
        vista.limpiar_pantalla()
        jugador = vista.elegir_pokemon()
        rivales = []
        for nombre in modelo.POKEDEX:
            rivales.append(nombre)
        enemigo = modelo.Pokemon.crear(random.choice(rivales))
        controlador.batalla(jugador, enemigo)
        respuesta = input("¿Jugar de nuevo? (s/n): ")
        if respuesta != "s" and respuesta != "S":
            break
    print("¡Hasta la próxima!")

main()