# modelo.py

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
    # el rango del daño: el minimo es el poder base y el maximo depende de la eficacia
    multiplicador = multiplicador_tipo(tipo_atacante, tipo_defensor)
    if multiplicador < 1:
        # matchup debil: el daño baja hasta la mitad, el maximo es el poder base
        minimo = int(base * multiplicador)
        maximo = base
    elif multiplicador > 1:
        # matchup fuerte: el minimo es el poder base, el maximo sube hasta base y media
        minimo = base
        maximo = int(base * multiplicador)
    else:
        # matchup neutral: el daño es siempre el poder base
        minimo = base
        maximo = base
    return minimo, maximo

def dano_aleatorio(base, tipo_atacante, tipo_defensor):
    # tira al azar un valor dentro del rango de daño
    minimo, maximo = rango_dano(base, tipo_atacante, tipo_defensor)
    return random.randint(minimo, maximo)

class Pokemon():
    # un combatiente: vida, tipo, habilidades y pasivas activas
    def __init__(self, nombre, tipo, vida, habilidades):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__vida_max = vida
        self.__vida = vida
        self.__nivel = 1
        self.__habilidades = habilidades
        self.__efectos = []  # pasivas activas sobre este pokemon

    def get_nombre(self):
        return self.__nombre
    nombre = property(fget=get_nombre)

    def get_tipo(self):
        return self.__tipo
    tipo = property(fget=get_tipo)

    def get_vida_max(self):
        return self.__vida_max
    vida_max = property(fget=get_vida_max)

    def get_vida(self):
        return self.__vida
    
    def set_vida(self, nueva_vida):
        if nueva_vida < 0:
            self.__vida = 0
        else:
            self.__vida = nueva_vida
    vida = property(fget=get_vida,fset=set_vida)

    def get_habilidades(self):
        return self.__habilidades
    habilidades = property(fget=get_habilidades)

    def get_efectos(self):
        return self.__efectos
    def set_efectos(self,efectos):
        self.__efectos = efectos
    efectos = property(fget=get_efectos,fset=set_efectos)

    def calcular_dano(self, habilidad, rival):
        # daño del golpe: tiro al azar entre base y base x eficacia
        base = habilidad["poder"] * self.__nivel
        return dano_aleatorio(base, self.__tipo, rival.tipo)

    def atacar(self, nombre_habilidad, rival):
        # aplica el daño de un ataque y lo resta al rival
        dano = self.calcular_dano(self.__habilidades[nombre_habilidad], rival)
        rival.vida = rival.vida - dano
        return dano

    def esta_activo(self, nombre_habilidad):
        # True si una pasiva con ese nombre ya esta activa
        for efecto in self.__efectos:
            if efecto["nombre"] == nombre_habilidad:
                return True
        return False

    def activar_pasiva(self, nombre_habilidad, rival):
        # activa una pasiva y devuelve "activa", "repetido" o "inmune"
        habilidad = self.__habilidades[nombre_habilidad]
        if habilidad["dano"] > 0:
            # RUTA 1: pasiva de daño (ej: Quemadura) -> el efecto se le aplica AL RIVAL
            if rival.tipo == "fuego":
                # los pokemon fuego no se queman
                return "inmune"
            if rival.esta_activo(nombre_habilidad):
                # no se acumula la misma pasiva dos veces
                return "repetido"
            rival.efectos.append({
                "nombre": nombre_habilidad,
                "dano": habilidad["dano"],
                "cura": habilidad["cura"],
                "turnos": habilidad["duracion"],
                "tipo_activador": self.__tipo
            })
            return "activa"
        # RUTA 2: pasiva de cura (ej: Hidrocuracion) -> el efecto se aplica A SI MISMO
        if self.esta_activo(nombre_habilidad):
            # no se acumula la misma pasiva dos veces
            return "repetido"
        self.__efectos.append({
            "nombre": nombre_habilidad,
            "dano": habilidad["dano"],
            "cura": habilidad["cura"],
            "turnos": habilidad["duracion"],
            "tipo_activador": self.__tipo
        })
        return "activa"

    def aplicar_efectos(self):
        # aplica el daño o la cura de cada pasiva activa, descuenta turnos
        # y devuelve una lista de eventos (datos sueltos, sin colores)
        eventos = []
        efectos_que_sobreviven = []
        for efecto in self.__efectos:
            if efecto["dano"] > 0:
                # el daño por turno tambien rueda al azar en su rango
                dano = dano_aleatorio(efecto["dano"], efecto["tipo_activador"], self.__tipo)
                self.__vida = self.__vida - dano
                eventos.append({
                    "nombre": self.__nombre,
                    "tipo": "dano",
                    "cantidad": dano,
                    "causa": efecto["nombre"]
                })
            if efecto["cura"] > 0:
                # la cura no pasa del tope de vida: se recorta lo que sobra
                curado = 0
                if self.__vida < self.__vida_max:
                    curado = efecto["cura"]
                    if self.__vida + curado > self.__vida_max:
                        curado = self.__vida_max - self.__vida
                self.__vida = self.__vida + curado
                if curado > 0:
                    # con vida llena no hay evento: "recupera 0" seria ruido
                    eventos.append({
                        "nombre": self.__nombre,
                        "tipo": "cura",
                        "cantidad": curado,
                        "causa": efecto["nombre"]
                    })
            # la pasiva pierde un turno y se elimina si ya expiro
            efecto["turnos"] = efecto["turnos"] - 1
            if efecto["turnos"] > 0:
                efectos_que_sobreviven.append(efecto)
        self.__efectos = efectos_que_sobreviven
        return eventos

    def esta_debilitado(self):
        # el pokemon cae cuando su vida llega a cero o menos
        return self.__vida <= 0

    @classmethod
    def crear(cls, nombre):
        # fabrica un pokemon a partir de sus datos de la pokedex
        datos = POKEDEX[nombre]
        return cls(nombre, datos["tipo"], datos["vida"], datos["habilidades"])