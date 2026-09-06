# =====================================================
# CONTROLADOR: turnos, IA del enemigo y flujo de partidas
# =====================================================

import random
import modelo
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
            # pasiva de daño: solo sirve contra no-fuego sin la quemadura activa
            sirve = jugador.tipo != "fuego" and not jugador.esta_activo(pasiva)
        else:
            # pasiva de cura: solo sirve si el enemigo no la tiene ya activa
            sirve = not enemigo.esta_activo(pasiva)
        if sirve and random.random() < 0.5:
            return pasiva
    return random.choice(ataques)

def batalla(jugador, enemigo):
    # combate por turnos completo hasta que uno (o ambos) se debilita
    vista.limpiar_pantalla()
    print("¡Un " + enemigo.nombre + " salvaje apareció!")
    print("¡Enfréntate a él con tu " + jugador.nombre + "!")

    # estado inicial (todavia no hay acciones que comentar)
    vista.mostrar_cuadro(jugador, enemigo, [], [])

    while True:
        # 3 grupos por columna para que el orden sea simetrico: propio, ajeno, reaccion
        efectos_jugador = []
        efectos_enemigo = []
        acciones_jugador = []
        acciones_enemigo = []
        reacciones_jugador = []
        reacciones_enemigo = []
        dano_jugador = 0  # daño que recibio tu pokemon este turno (rojo en la barra)
        dano_enemigo = 0  # daño que recibio el rival este turno (rojo en su barra)

        # 1) efectos pasivos de ambos al inicio del turno
        for dato in jugador.aplicar_efectos():
            efectos_jugador.append(vista.armar_efecto(dato))
            if dato["tipo"] == "cura":
                # tu curacion tambien se anota en la columna del rival
                efectos_enemigo.append(vista.armar_curacion_ajena(dato["nombre"], dato["causa"], dato["cantidad"]))
        for dato in enemigo.aplicar_efectos():
            efectos_enemigo.append(vista.armar_efecto(dato))
            if dato["tipo"] == "cura":
                # la curacion del rival tambien se anota en tu columna
                efectos_jugador.append(vista.armar_curacion_ajena(dato["nombre"], dato["causa"], dato["cantidad"]))

        # 2) chequeo de debilitamiento por efectos
        if jugador.esta_muerto() and enemigo.esta_muerto():
            vista.limpiar_pantalla()
            vista.mostrar_cuadro(jugador, enemigo, efectos_jugador, efectos_enemigo, dano_jugador, dano_enemigo)
            print("¡Ambos se debilitaron! ¡Empate!")
            return
        if jugador.esta_muerto():
            vista.limpiar_pantalla()
            vista.mostrar_cuadro(jugador, enemigo, efectos_jugador, efectos_enemigo, dano_jugador, dano_enemigo)
            print("¡" + jugador.nombre + " se debilitó! ¡Perdiste!")
            return
        if enemigo.esta_muerto():
            vista.limpiar_pantalla()
            vista.mostrar_cuadro(jugador, enemigo, efectos_jugador, efectos_enemigo, dano_jugador, dano_enemigo)
            print("¡" + enemigo.nombre + " se debilitó! ¡Ganaste!")
            return

        # 3) turno del jugador: escribir el movimiento confirma que leyo el turno anterior
        nombre = vista.elegir_habilidad(jugador, enemigo)
        habilidad = jugador.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            # ataque instantaneo: golpea al rival
            dano = jugador.atacar(nombre, enemigo)
            dano_enemigo = dano
            acciones_jugador.append(vista.armar_uso("Tu", jugador, nombre, dano))
            reacciones_enemigo.append(vista.armar_sufrir("El", enemigo, nombre, dano))
        else:
            # pasiva: el daño va al rival, la cura a si mismo
            resultado = jugador.efecto(nombre, enemigo)
            if resultado == "activa":
                acciones_jugador.append(vista.armar_activa("Tu", jugador, nombre, habilidad["duracion"]))
            if resultado == "repetido":
                acciones_jugador.append(nombre + " ya está activo. Turno perdido.")
            if resultado == "inmune":
                acciones_jugador.append(nombre + " no afecta a " + enemigo.nombre + " (tipo fuego).")

        if enemigo.esta_muerto():
            # fin por victoria
            vista.limpiar_pantalla()
            vista.mostrar_cuadro(jugador, enemigo, efectos_jugador + acciones_jugador + reacciones_jugador, efectos_enemigo + acciones_enemigo + reacciones_enemigo, dano_jugador, dano_enemigo)
            print("¡" + enemigo.nombre + " se debilitó! ¡Ganaste!")
            return

        # 4) turno del enemigo: la IA elige su habilidad
        nombre = elegir_movimiento_enemigo(enemigo, jugador)
        habilidad = enemigo.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            # ataque del enemigo: golpea a tu pokemon
            dano = enemigo.atacar(nombre, jugador)
            dano_jugador = dano
            acciones_enemigo.append(vista.armar_uso("El", enemigo, nombre, dano))
            reacciones_jugador.append(vista.armar_sufrir("Tu", jugador, nombre, dano))
        else:
            # pasiva del enemigo: el daño va a tu pokemon, la cura a si mismo
            resultado = enemigo.efecto(nombre, jugador)
            if resultado == "activa":
                acciones_enemigo.append(vista.armar_activa("El", enemigo, nombre, habilidad["duracion"]))
            if resultado == "inmune":
                acciones_enemigo.append(nombre + " no afecta a " + jugador.nombre + " (tipo fuego).")

        if jugador.esta_muerto():
            # fin por derrota
            vista.limpiar_pantalla()
            vista.mostrar_cuadro(jugador, enemigo, efectos_jugador + acciones_jugador + reacciones_jugador, efectos_enemigo + acciones_enemigo + reacciones_enemigo, dano_jugador, dano_enemigo)
            print("¡" + jugador.nombre + " se debilitó! ¡Perdiste!")
            return

        # 5) fotograma del turno: resultado completo y menu al final
        vista.limpiar_pantalla()
        vista.mostrar_cuadro(jugador, enemigo, efectos_jugador + acciones_jugador + reacciones_jugador, efectos_enemigo + acciones_enemigo + reacciones_enemigo, dano_jugador, dano_enemigo)

