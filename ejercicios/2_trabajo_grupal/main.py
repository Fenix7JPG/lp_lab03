# =====================================================
# ENTRADA: este fichero solo ARRANCA el juego
# Ejecutar con:  python main.py
# =====================================================

import random
import controlador
import modelo
import vista

def main():
    # bucle principal: elegir pokemon, batallar y preguntar revancha
    vista.activar_colores()
    print("=== POKEMON 1vs1 ===")
    while True:
        vista.limpiar_pantalla()
        jugador = vista.elegir_pokemon()
        # el rival se elige al azar entre todos los nombres de la pokedex
        rivales = []
        for nombre in modelo.POKEDEX:
            rivales.append(nombre)
        enemigo = modelo.Pokemon.crear(random.choice(rivales))
        controlador.batalla(jugador, enemigo)
        respuesta = input("¿Jugar de nuevo? (s/n): ")
        if respuesta != "s" and respuesta != "S":
            # cualquier cosa distinta de "s" o "S" cierra el juego
            break
    print("¡Hasta la próxima!")

# este if solo es verdad cuando ejecutas el fichero directamente
if __name__ == "__main__":
    main()