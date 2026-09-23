# controlador.py

import random
import vista
from pokedex import POKEDEX
import modelo
def elegir_movimiento_enemigo(enemigo, jugador):
    # IA: usa su pasiva si es util (50%), si no ataca al azar
    ataques = []
    pasiva = ""
    for nombre in enemigo.habilidades:
        habilidad = enemigo.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            ataques.append(nombre)
        else:
            pasiva = nombre
    if pasiva != "":
        habilidad = enemigo.habilidades[pasiva]
        if habilidad["dano"] > 0:
            # pasiva de daño: solo sirve contra pokemon no fuego y sin la quemadura activa
            sirve = jugador.tipo != "fuego" and not jugador.esta_activo(pasiva)
        else:
            # pasiva de cura: solo sirve si el enemigo no la tiene ya activa
            sirve = not enemigo.esta_activo(pasiva)
        if sirve and random.random() < 0.5:
            return pasiva
    return random.choice(ataques)

def elegir_pokemon_alazar():
    rivales = []
    for nombre in POKEDEX:
        rivales.append(nombre)
    return modelo.Pokemon.crear(random.choice(rivales))


def elegir_pokemon():
    nombres = []

    for nombre in modelo.POKEDEX:
        nombres.append(nombre)

    vista.menu_pokemon(nombres)
    
    while True:
        opcion = vista.pedir_opcion_pokemon() 
        try:
            numero = int(opcion)
        except ValueError:
            vista.mostrar_error_input_invalido()
            continue
            
        if numero >= 1 and numero <= len(nombres):
            nombre_elegido = nombres[numero - 1]
            return modelo.Pokemon.crear(nombre_elegido)  
            
        vista.mostrar_error_rango(len(nombres))

def elegir_habilidad(pokemon, rival):
    # Extraemos los nombres de las habilidades con un bucle for clásico
    nombres = []
    for nombre in pokemon.habilidades:
        nombres.append(nombre)
        
    # Le ordenamos a la vista imprimir el encabezado del menú
    vista.mostrar_encabezado_habilidades(pokemon.nombre)
    
    # 3. Calculamos los datos de cada habilidad y le pedimos a la vista que los pinte
    i = 1
    for nombre in nombres:
        habilidad = pokemon.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            # Le pedimos al modelo el cálculo matemático
            minimo, maximo = modelo.rango_dano(habilidad["poder"], pokemon.tipo, rival.tipo)
            vista.mostrar_opcion_ataque(i, nombre, minimo, maximo)
        else:
            vista.mostrar_opcion_efecto(i, nombre, habilidad["duracion"])
        i = i + 1
        
    # 4. Bucle de validación del controlador (El cerebro del menú)
    while True:
        opcion = vista.pedir_movimiento()
        try:
            numero = int(opcion)
        except ValueError:
            vista.mostrar_error_numero_valido()
            continue
        if numero >= 1 and numero <= len(nombres):
            return nombres[numero - 1]
        vista.mostrar_error_rango_habilidades(len(nombres))



def batalla(jugador, enemigo):
    # combate por turnos con un log cronológico hasta que uno (o ambos) cae
    vista.limpiar_pantalla()
    vista.mostrar_inicio_combate(jugador.nombre, enemigo.nombre)

    # estado inicial (log vacío)
    vista.mostrar_turno(jugador, enemigo, [])

    while True:
        # el log del turno: una lista ÚNICA donde cada acción ocupa una línea
        eventos = []
        dano_jugador = 0  # daño que RECIBIÓ tu pokemon este turno
        dano_enemigo = 0  # daño que RECIBIÓ el rival este turno

        # efectos pasivos de ambos al inicio del turno
        for dato in jugador.aplicar_efectos():
            eventos.append(vista.evento_efecto(dato, False))
        for dato in enemigo.aplicar_efectos():
            eventos.append(vista.evento_efecto(dato, True))

        # chequeo de debilitamiento por efectos
        if jugador.esta_debilitado() and enemigo.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            vista.mostrar_resultado_empate()
            return
        if jugador.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            vista.mostrar_resultado_derrota(jugador.nombre)
            return
        if enemigo.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            vista.mostrar_resultado_victoria(enemigo.nombre)
            return

        # turno del jugador
        nombre = elegir_habilidad(jugador, enemigo)
        habilidad = jugador.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            dano = jugador.atacar(nombre, enemigo)
            dano_enemigo = dano
            eventos.append(vista.evento_uso(jugador, enemigo, nombre, dano))
        else:
            resultado = jugador.activar_pasiva(nombre, enemigo)
            if resultado == "activa":
                eventos.append(vista.evento_activa(jugador, nombre, habilidad["duracion"]))
            elif resultado == "repetido":
                eventos.append(vista.evento_repetido(nombre))
            elif resultado == "inmune":
                eventos.append(vista.evento_inmune(enemigo, nombre))

        if enemigo.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            vista.mostrar_resultado_victoria(enemigo.nombre)
            return

        # turno del enemigo (IA)
        nombre = elegir_movimiento_enemigo(enemigo, jugador)
        habilidad = enemigo.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            dano = enemigo.atacar(nombre, jugador)
            dano_jugador = dano
            eventos.append(vista.evento_uso(enemigo, jugador, nombre, dano))
        else:
            resultado = enemigo.activar_pasiva(nombre, jugador)
            if resultado == "activa":
                eventos.append(vista.evento_activa(enemigo, nombre, habilidad["duracion"]))
            elif resultado == "inmune":
                eventos.append(vista.evento_inmune(jugador, nombre))

        if jugador.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            vista.mostrar_resultado_derrota(jugador.nombre)
            return

        # 5) fotograma del turno: log completo y menú al final
        vista.limpiar_pantalla()
        vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
