# vista.py

import modelo

# colores ANSI: amarillo causa, rojo sufre, verde se cura, cian se cura el rival

NORMAL = "\033[0m"

def rojo(texto):
    return "\033[91m" + texto + NORMAL

def verde(texto):
    return "\033[92m" + texto + NORMAL

def amarillo(texto):
    return "\033[93m" + texto + NORMAL

def cian(texto):
    return "\033[96m" + texto + NORMAL

def rojo_titulo(texto):
    return "\033[38;2;255;0;0m" + texto + NORMAL

def rojo_titulo(texto):
    return "\033[38;2;255;0;0m" + texto + NORMAL

def naranja_titulo(texto):
    return "\033[38;2;255;80;40m" + texto + NORMAL

def salmon_titulo(texto):
    return "\033[38;2;255;140;90m" + texto + NORMAL

def melocoton_titulo(texto):
    return "\033[38;2;255;190;150m" + texto + NORMAL

def casi_blanco_titulo(texto):
    return "\033[38;2;255;230;215m" + texto + NORMAL

def blanco_titulo(texto):
    return "\033[38;2;255;255;255m" + texto + NORMAL

def limpiar_pantalla():
    # empuja el fotograma anterior fuera de la pantalla
    i = 0
    while i < 40:
        print("")
        i = i + 1

def barra_vida(pokemon, dano_reciente):
    # barra de 12 celdas: verde = vida, rojo = daño recibido este turno, puntos = daño viejo
    celdas = 12
    # celdas verdes: la vida actual sobre la vida maxima
    llenas = pokemon.vida * celdas // pokemon.vida_max
    if llenas < 0:
        llenas = 0
    if llenas > celdas:
        llenas = celdas
    # celdas rojas: el daño que acaba de llegar en este turno
    rojas = dano_reciente * celdas // pokemon.vida_max
    if rojas < 0:
        rojas = 0
    if llenas + rojas > celdas:
        # nunca se sale de la barra: el rojo se recorta si no cabe
        rojas = celdas - llenas
    # celdas en puntos: el daño de turnos anteriores (ya no se resalta)
    viejas = celdas - llenas - rojas
    barra = ""
    if llenas > 0:
        barra = verde("#" * llenas)
    if rojas > 0:
        barra = barra + rojo("#" * rojas)
    return barra + "." * viejas

def mostrar_turno(jugador, enemigo, eventos, dano_jugador=0, dano_enemigo=0):
    # fotograma del turno: estado de ambos arriba y debajo un solo log de eventos
    # dano_jugador / dano_enemigo = daño que cada uno RECIBIO este turno (rojo en su barra)
    print()
    print("TU POKEMON : " + jugador.nombre + " (" + jugador.tipo + ") " + barra_vida(jugador, dano_jugador) + " " + verde(str(jugador.vida)) + "/" + str(jugador.vida_max))
    print("RIVAL      : " + enemigo.nombre + " (" + enemigo.tipo + ") " + barra_vida(enemigo, dano_enemigo) + " " + verde(str(enemigo.vida)) + "/" + str(enemigo.vida_max))
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
    # arma la linea de un efecto pasivo (dato viene del modelo)
    # es_rival: True cuando el efecto le paso al pokemon del rival (lo sabe el controlador,
    # la vista no puede comparar nombres porque dos pokemons podrian llamarse igual)
    if dato["tipo"] == "dano":
        # quien sufre el daño va en rojo
        return dato["nombre"] + " sufre " + rojo(str(dato["cantidad"])) + " de daño por " + dato["causa"]
    if es_rival:
        # la curacion del rival va en cian, para no confundirla con la propia
        return "El " + dato["nombre"] + " rival recupera " + cian(str(dato["cantidad"])) + " de vida por " + dato["causa"]
    # la curacion propia va en verde
    return dato["nombre"] + " recupera " + verde(str(dato["cantidad"])) + " de vida por " + dato["causa"]


def mostrar_titulo_juego():
    limpiar_pantalla()
    
    print()
    print(rojo_titulo("██████╗░░█████╗░██╗░░██╗███████╗███╗░░░███╗░█████╗░███╗░░██╗"))
    print(rojo_titulo("██╔══██╗██╔══██╗██║░██╔╝██╔════╝████╗░████║██╔══██╗████╗░██║"))
    print(naranja_titulo("██████╔╝██║░░██║█████═╝░█████╗░░██╔████╔██║██║░░██║██╔██╗██║"))
    print(salmon_titulo("██╔═══╝░██║░░██║██╔═██╗░██╔══╝░░██║╚██╔╝██║██║░░██║██║╚████║"))
    print(melocoton_titulo("██║░░░░░╚█████╔╝██║░╚██╗███████╗██║░╚═╝░██║╚█████╔╝██║░╚███║"))
    print(blanco_titulo("╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝"))
    print()

def menu_pokemon(nombres):
    # Construir la lista de items (texto de cada opción)
    items = []
    i = 1
    for nombre in nombres:
        datos = modelo.POKEDEX[nombre]
        tipo = datos["tipo"]
        texto = str(i) + ") " + nombre + " (" + tipo + ")"
        items.append(texto)
        i = i + 1
    
    # Calcular el ancho del contenido (el texto más largo)
    titulo = "ELIGE TU POKEMON"
    ancho_max = len(titulo)
    for item in items:
        if len(item) > ancho_max:
            ancho_max = len(item)
    
    # El marco tiene 2 espacios de padding a cada lado
    ancho = ancho_max + 4
    
    # Dibujar la parte de arriba del marco
    print("")
    print("┌" + "─" * ancho + "┐")
    
    # Dibujar el título centrado
    espacios_izq = (ancho - len(titulo)) // 2
    espacios_der = ancho - len(titulo) - espacios_izq
    print("│" + " " * espacios_izq + titulo + " " * espacios_der + "│")
    
    # Línea separadora
    print("├" + "─" * ancho + "┤")
    
    # Dibujar cada item dentro del marco
    for item in items:
        espacios_der = ancho - 2 - len(item)  # 2 = padding izquierdo
        print("│  " + item + " " * espacios_der + "│")
    
    # Cerrar el marco
    print("└" + "─" * ancho + "┘")
    print("")

def pedir_opcion_pokemon():
    opcion = input("Introduce el numero de tu pokemon favorito:")
    return opcion

def mostrar_encabezado_habilidades(nombre_pokemon):
    print("HABILIDADES DE " + nombre_pokemon +" : ")

def mostrar_opcion_ataque(indice, nombre, minimo, maximo):
    print("  " + str(indice) + ") " + nombre + " (daño " + str(minimo) + " a " + str(maximo) + ")")

def mostrar_opcion_efecto(indice, nombre, duracion):
    print("  " + str(indice) + ") " + nombre + " (efecto, " + str(duracion) + " turnos)")

def pedir_movimiento():
    return input("Movimiento: ")

def mostrar_error_numero_valido():
    print("Escribe un número válido.")

def mostrar_error_rango_habilidades(total_habilidades):
    print("Elige un número entre 1 y " + str(total_habilidades) + ".")


def mostrar_inicio_combate(nombre_jugador, nombre_enemigo):
    print()
    print("¡Un " + nombre_enemigo + " salvaje apareció!")
    print("¡Enfréntate a él con tu " + nombre_jugador + "!")

def mostrar_resultado_empate():
    print("¡Ambos se debilitaron! ¡Empate!")

def mostrar_resultado_derrota(nombre_jugador):
    print("¡" + nombre_jugador + " se debilitó! ¡Perdiste!")

def mostrar_resultado_victoria(nombre_enemigo):
    print("¡" + nombre_enemigo + " se debilitó! ¡Ganaste!")

def fin():
    print("¡Fin del juego!")