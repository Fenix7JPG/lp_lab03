# main.py

import random
import controlador
import modelo
import vista

def main():
    while True:
        vista.mostrar_titulo_juego()
        jugador = controlador.elegir_pokemon()
        enemigo = controlador.elegir_pokemon_alazar()

        controlador.batalla(jugador, enemigo)
        respuesta = input("¿Jugar de nuevo? (s/n): ")

        if respuesta.lower() != "s":
            break
    vista.fin()

if __name__ == "__main__":
    main()