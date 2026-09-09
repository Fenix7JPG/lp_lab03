# =====================================================
# VISTA: muestra pantalla y pide datos (no cambia estado)
# =====================================================

import modelo

# colores ANSI: amarillo causa, rojo sufre, verde se cura, cian se cura el rival
ROJO = "\033[91m"
VERDE_CLARO = "\033[92m"
CIAN = "\033[96m"
AMARILLO = "\033[93m"
NORMAL = "\033[0m"

def activar_colores():
    # habilita los colores ANSI en la consola de Windows
    import os
    if os.name == "nt":
        os.system("")

def limpiar_pantalla():
    # empuja el fotograma anterior fuera de la pantalla
    i = 0
    while i < 40:
        print("")
        i = i + 1

def rojo(texto):
    return ROJO + texto + NORMAL

def verde(texto):
    return VERDE_CLARO + texto + NORMAL

def amarillo(texto):
    return AMARILLO + texto + NORMAL

def cian(texto):
    return CIAN + texto + NORMAL

def vida_visible(pokemon):
    # nunca muestra vida negativa
    if pokemon.vida < 0:
        return 0
    return pokemon.vida

def barra_vida(pokemon, dano_reciente):
    # barra de 12 celdas: verde = vida, rojo = daño del turno, puntos = daño viejo
    celdas = 12
    llenas = vida_visible(pokemon) * celdas // pokemon.vida_max
    if llenas < 0:
        llenas = 0
    if llenas > celdas:
        llenas = celdas
    rojas = dano_reciente * celdas // pokemon.vida_max
    if rojas < 0:
        rojas = 0
    if llenas + rojas > celdas:
        rojas = celdas - llenas
    viejas = celdas - llenas - rojas
    barra = ""
    if llenas > 0:
        barra = verde("#" * llenas)
    if rojas > 0:
        barra = barra + rojo("#" * rojas)
    return barra + "." * viejas

def mostrar_turno(jugador, enemigo, eventos, dano_jugador=0, dano_enemigo=0):
    # fotograma del turno: estado de ambos arriba y un unico log debajo
    print()
    print("TU POKEMON : " + jugador.nombre + " (" + jugador.tipo + ") " + barra_vida(jugador, dano_jugador) + " " + verde(str(vida_visible(jugador)) + "/" + str(jugador.vida_max)))
    print("RIVAL      : " + enemigo.nombre + " (" + enemigo.tipo + ") " + barra_vida(enemigo, dano_enemigo) + " " + verde(str(vida_visible(enemigo)) + "/" + str(enemigo.vida_max)))
    print()
    for evento in eventos:
        print("     " + evento)
    print()

def evento_uso(atacante, defensor, habilidad, dano):
    # ataque: quien ataca, cuanto y a quien (causa = amarillo)
    return atacante.nombre + " usa " + habilidad + " y causa " + amarillo(str(dano)) + " de daño a " + defensor.nombre + "!"

def evento_activa(pokemon, habilidad, duracion):
    # activacion de una pasiva
    return pokemon.nombre + " activa " + habilidad + " durante " + str(duracion) + " turnos!"

def evento_repetido(habilidad):
    # aviso de pasiva ya activa
    return habilidad + " ya está activo. Turno perdido."

def evento_inmune(objetivo, habilidad):
    # aviso de inmunidad (fuego no se quema)
    return habilidad + " no afecta a " + objetivo.nombre + " (tipo fuego)."

def evento_efecto(dato, es_rival):
    # efecto pasivo aplicado (dato del modelo); es_rival=True pinta la curacion en cian
    if dato["tipo"] == "dano":
        # el daño que sufre (rojo)
        return dato["nombre"] + " sufre " + rojo(str(dato["cantidad"])) + " de daño por " + dato["causa"]
    if es_rival:
        # la curacion del rival (cian)
        return "El " + dato["nombre"] + " rival recupera " + cian(str(dato["cantidad"])) + " de vida por " + dato["causa"]
    # la curacion propia (verde)
    return dato["nombre"] + " recupera " + verde(str(dato["cantidad"])) + " de vida por " + dato["causa"]

def elegir_pokemon():
    # menu de eleccion de pokemon; devuelve el Pokemon creado
    nombres = []
    for nombre in modelo.POKEDEX:
        nombres.append(nombre)
    print()
    print("ELIGE TU POKEMON:")
    i = 1
    for nombre in nombres:
        datos = modelo.POKEDEX[nombre]
        print("  " + str(i) + ") " + nombre + " (" + datos["tipo"] + ")")
        i = i + 1
    while True:
        opcion = input("Número: ")
        try:
            numero = int(opcion)
        except ValueError:
            print("Escribe un número válido.")
            continue
        if numero >= 1 and numero <= len(nombres):
            return modelo.Pokemon.crear(nombres[numero - 1])
        print("Elige un número entre 1 y " + str(len(nombres)) + ".")

def elegir_habilidad(pokemon, rival):
    # menu de habilidades con rango de daño contra el rival; devuelve el nombre elegido
    nombres = []
    for nombre in pokemon.habilidades:
        nombres.append(nombre)
    print("HABILIDADES DE " + pokemon.nombre + " (vs " + rival.nombre + "):")
    i = 1
    for nombre in nombres:
        habilidad = pokemon.habilidades[nombre]
        if habilidad["tipo"] == "ataque":
            minimo, maximo = modelo.rango_dano(habilidad["poder"], pokemon.tipo, rival.tipo)
            print("  " + str(i) + ") " + nombre + " (daño " + str(minimo) + " a " + str(maximo) + ")")
        else:
            print("  " + str(i) + ") " + nombre + " (efecto, " + str(habilidad["duracion"]) + " turnos)")
        i = i + 1
    while True:
        opcion = input("Movimiento: ")
        try:
            numero = int(opcion)
        except ValueError:
            print("Escribe un número válido.")
            continue
        if numero >= 1 and numero <= len(nombres):
            return nombres[numero - 1]
        print("Elige un número entre 1 y " + str(len(nombres)) + ".")