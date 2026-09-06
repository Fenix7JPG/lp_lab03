# =====================================================
# MODELO: reglas y estado del juego (sin interfaz)
# =====================================================

import random
from pokedex import POKEDEX

def multiplicador_tipo(ataque, defensa):
    # 1.5 si el ataque es fuerte contra la defensa, 0.5 si es debil, 1 si es neutral
    if ataque == "fuego" and defensa == "planta":
        return 1.5
    if ataque == "fuego" and defensa == "agua":
        return 0.5
    if ataque == "agua" and defensa == "fuego":
        return 1.5
    if ataque == "agua" and defensa == "planta":
        return 0.5
    if ataque == "planta" and defensa == "agua":
        return 1.5
    if ataque == "planta" and defensa == "fuego":
        return 0.5
    return 1

def rango_dano(base, tipo_atacante, tipo_defensor):
    # rango del daño: min = base, max = base x eficacia (ordenado)
    multiplicador = multiplicador_tipo(tipo_atacante, tipo_defensor)
    minimo = int(base * min(multiplicador, 1.0))
    maximo = int(base * max(multiplicador, 1.0))
    return minimo, maximo

def dano_aleatorio(base, tipo_atacante, tipo_defensor):
    # tira al azar un valor dentro del rango de daño
    minimo, maximo = rango_dano(base, tipo_atacante, tipo_defensor)
    return random.randint(minimo, maximo)

class Pokemon():
    # un combatiente: vida, tipo, habilidades y pasivas activas
    def __init__(self, nombre, tipo, vida, habilidades):
        self.nombre = nombre
        self.tipo = tipo
        self.vida_max = vida
        self.vida = vida
        self.nivel = 1
        self.habilidades = habilidades
        self.efectos = []  # pasivas activas sobre este pokemon

    def daño(self, habilidad, rival):
        # daño del golpe: tiro al azar entre base y base x eficacia
        base = habilidad["poder"] * self.nivel
        return dano_aleatorio(base, self.tipo, rival.tipo)

    def atacar(self, nombre_habilidad, rival):
        # aplica el daño de un ataque y lo resta al rival
        dano = self.daño(self.habilidades[nombre_habilidad], rival)
        rival.vida = rival.vida - dano
        return dano

    def esta_activo(self, nombre_habilidad):
        # True si una pasiva con ese nombre ya esta activa
        for efecto in self.efectos:
            if efecto["nombre"] == nombre_habilidad:
                return True
        return False

    def efecto(self, nombre_habilidad, rival):
        # activa una pasiva (daño va al rival, cura a si mismo); devuelve activa/repetido/inmune
        habilidad = self.habilidades[nombre_habilidad]
        if habilidad["dano"] > 0:
            if rival.tipo == "fuego":
                return "inmune"  # los pokemon fuego no se queman
            if rival.esta_activo(nombre_habilidad):
                return "repetido"
            rival.efectos.append({
                "nombre": nombre_habilidad,
                "dano": habilidad["dano"],
                "cura": habilidad["cura"],
                "turnos": habilidad["duracion"],
                "tipo_activador": self.tipo
            })
            return "activa"
        if self.esta_activo(nombre_habilidad):
            return "repetido"
        self.efectos.append({
            "nombre": nombre_habilidad,
            "dano": habilidad["dano"],
            "cura": habilidad["cura"],
            "turnos": habilidad["duracion"],
            "tipo_activador": self.tipo
        })
        return "activa"

    def aplicar_efectos(self):
        # aplica daño/cura de cada pasiva activa, descuenta turnos y devuelve datos sin colores
        mensajes = []
        sobrevivientes = []
        for efecto in self.efectos:
            if efecto["dano"] > 0:
                # el daño por turno tambien rueda en su rango
                dano = dano_aleatorio(efecto["dano"], efecto["tipo_activador"], self.tipo)
                self.vida = self.vida - dano
                mensajes.append({
                    "nombre": self.nombre,
                    "tipo": "dano",
                    "cantidad": dano,
                    "causa": efecto["nombre"]
                })
            if efecto["cura"] > 0:
                curado = 0
                if self.vida < self.vida_max:
                    curado = efecto["cura"]
                    if self.vida + curado > self.vida_max:
                        curado = self.vida_max - self.vida
                self.vida = self.vida + curado
                if curado > 0:
                    # vida llena no emite mensaje: recupera 0 es ruido
                    mensajes.append({
                        "nombre": self.nombre,
                        "tipo": "cura",
                        "cantidad": curado,
                        "causa": efecto["nombre"]
                    })
            efecto["turnos"] = efecto["turnos"] - 1
            if efecto["turnos"] > 0:
                sobrevivientes.append(efecto)
        self.efectos = sobrevivientes
        return mensajes

    def esta_muerto(self):
        # debilitado cuando la vida llega a cero o menos
        return self.vida <= 0

    @classmethod
    def crear(cls, nombre):
        # fabrica un pokemon a partir de la pokedex
        datos = POKEDEX[nombre]
        return cls(nombre, datos["tipo"], datos["vida"], datos["habilidades"])