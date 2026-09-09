# =====================================================
# CONTROLADOR: turnos, IA del enemigo y log de eventos
# =====================================================

import random
import vista

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

def batalla(jugador, enemigo):
    # combate por turnos con un log cronologico hasta que uno (o ambos) cae
    vista.limpiar_pantalla()
    print("¡Un " + enemigo.nombre + " salvaje apareció!")
    print("¡Enfréntate a él con tu " + jugador.nombre + "!")

    # estado inicial (log vacio)
    vista.mostrar_turno(jugador, enemigo, [])

    while True:
        # el log del turno: una lista UNICA donde cada accion ocupa una linea
        eventos = []
        dano_jugador = 0  # daño que RECIBIO tu pokemon este turno (se pinta rojo en su barra)
        dano_enemigo = 0  # daño que RECIBIO el rival este turno (se pinta rojo en su barra)

        # 1) efectos pasivos de ambos al inicio del turno
        for dato in jugador.aplicar_efectos():
            # los efectos de TU pokemon no son del rival
            eventos.append(vista.evento_efecto(dato, False))
        for dato in enemigo.aplicar_efectos():
            # los efectos del RIVAL se marcan para que su cura salga en cian
            eventos.append(vista.evento_efecto(dato, True))

        # 2) chequeo de debilitamiento por efectos (empate, derrota o victoria)
        if jugador.esta_debilitado() and enemigo.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            print("¡Ambos se debilitaron! ¡Empate!")
            return
        if jugador.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            print("¡" + jugador.nombre + " se debilitó! ¡Perdiste!")
            return
        if enemigo.esta_debilitado():
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            print("¡" + enemigo.nombre + " se debilitó! ¡Ganaste!")
            return

        # 3) turno del jugador: escribir el movimiento confirma que ya leyo el turno anterior
        nombre = vista.elegir_habilidad(jugador, enemigo)
        habilidad = jugador.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            # ataque instantaneo: golpea al rival
            dano = jugador.atacar(nombre, enemigo)
            dano_enemigo = dano
            eventos.append(vista.evento_uso(jugador, enemigo, nombre, dano))
        else:
            # pasiva: el daño va al rival, la cura a si mismo
            resultado = jugador.activar_pasiva(nombre, enemigo)
            if resultado == "activa":
                eventos.append(vista.evento_activa(jugador, nombre, habilidad["duracion"]))
            if resultado == "repetido":
                eventos.append(vista.evento_repetido(nombre))
            if resultado == "inmune":
                eventos.append(vista.evento_inmune(enemigo, nombre))

        if enemigo.esta_debilitado():
            # fin por victoria: se muestra el turno y termina
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            print("¡" + enemigo.nombre + " se debilitó! ¡Ganaste!")
            return

        # 4) turno del enemigo: la IA elige su habilidad
        nombre = elegir_movimiento_enemigo(enemigo, jugador)
        habilidad = enemigo.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            # ataque del enemigo: golpea a tu pokemon
            dano = enemigo.atacar(nombre, jugador)
            dano_jugador = dano
            eventos.append(vista.evento_uso(enemigo, jugador, nombre, dano))
        else:
            # pasiva del enemigo: el daño va a tu pokemon, la cura a si mismo
            resultado = enemigo.activar_pasiva(nombre, jugador)
            if resultado == "activa":
                eventos.append(vista.evento_activa(enemigo, nombre, habilidad["duracion"]))
            if resultado == "inmune":
                eventos.append(vista.evento_inmune(jugador, nombre))

        if jugador.esta_debilitado():
            # fin por derrota: se muestra el turno y termina
            vista.limpiar_pantalla()
            vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)
            print("¡" + jugador.nombre + " se debilitó! ¡Perdiste!")
            return

        # 5) fotograma del turno: log completo y menu al final
        vista.limpiar_pantalla()
        vista.mostrar_turno(jugador, enemigo, eventos, dano_jugador, dano_enemigo)