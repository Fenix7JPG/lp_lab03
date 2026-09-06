# =====================================================
# POKEDEX: catalogo de datos de los pokemons
# 12 pokemons (4 por tipo), cada uno con 3 habilidades
# =====================================================

POKEDEX = {
    # ---------------- FUEGO ----------------
    "Charmander": {
        "tipo": "fuego",
        "vida": 110,
        "habilidades": {
            "Llamarada": {"tipo": "ataque", "poder": 40},
            "Ascuas": {"tipo": "ataque", "poder": 25},
            "Quemadura": {"tipo": "pasiva", "dano": 12, "cura": 0, "duracion": 3}
        }
    },
    "Vulpix": {
        "tipo": "fuego",
        "vida": 100,
        "habilidades": {
            "Fuego Fatuo": {"tipo": "ataque", "poder": 30},
            "Brasas": {"tipo": "ataque", "poder": 20},
            "Quemadura": {"tipo": "pasiva", "dano": 12, "cura": 0, "duracion": 3}
        }
    },
    "Growlithe": {
        "tipo": "fuego",
        "vida": 105,
        "habilidades": {
            "Colmillo Ígneo": {"tipo": "ataque", "poder": 35},
            "Rueda Fuego": {"tipo": "ataque", "poder": 30},
            "Quemadura": {"tipo": "pasiva", "dano": 12, "cura": 0, "duracion": 3}
        }
    },
    "Ponyta": {
        "tipo": "fuego",
        "vida": 95,
        "habilidades": {
            "Llamarada": {"tipo": "ataque", "poder": 40},
            "Doble Patada": {"tipo": "ataque", "poder": 25},
            "Quemadura": {"tipo": "pasiva", "dano": 12, "cura": 0, "duracion": 3}
        }
    },
    # ---------------- AGUA ----------------
    "Squirtle": {
        "tipo": "agua",
        "vida": 110,
        "habilidades": {
            "Pistola Agua": {"tipo": "ataque", "poder": 35},
            "Burbuja": {"tipo": "ataque", "poder": 25},
            "Hidrocuración": {"tipo": "pasiva", "dano": 0, "cura": 14, "duracion": 3}
        }
    },
    "Psyduck": {
        "tipo": "agua",
        "vida": 100,
        "habilidades": {
            "Rayo Burbuja": {"tipo": "ataque", "poder": 30},
            "Confusión": {"tipo": "ataque", "poder": 35},
            "Hidrocuración": {"tipo": "pasiva", "dano": 0, "cura": 14, "duracion": 3}
        }
    },
    "Staryu": {
        "tipo": "agua",
        "vida": 100,
        "habilidades": {
            "Rayo Burbuja": {"tipo": "ataque", "poder": 30},
            "Giro Rápido": {"tipo": "ataque", "poder": 25},
            "Hidrocuración": {"tipo": "pasiva", "dano": 0, "cura": 14, "duracion": 3}
        }
    },
    "Krabby": {
        "tipo": "agua",
        "vida": 105,
        "habilidades": {
            "Corte Furia": {"tipo": "ataque", "poder": 30},
            "Burbuja": {"tipo": "ataque", "poder": 25},
            "Hidrocuración": {"tipo": "pasiva", "dano": 0, "cura": 14, "duracion": 3}
        }
    },
    # ---------------- PLANTA ----------------
    "Bulbasaur": {
        "tipo": "planta",
        "vida": 115,
        "habilidades": {
            "Látigo Cepa": {"tipo": "ataque", "poder": 35},
            "Hoja Afilada": {"tipo": "ataque", "poder": 25},
            "Regeneración": {"tipo": "pasiva", "dano": 0, "cura": 12, "duracion": 3}
        }
    },
    "Oddish": {
        "tipo": "planta",
        "vida": 100,
        "habilidades": {
            "Absorber": {"tipo": "ataque", "poder": 30},
            "Hoja Afilada": {"tipo": "ataque", "poder": 20},
            "Regeneración": {"tipo": "pasiva", "dano": 0, "cura": 12, "duracion": 3}
        }
    },
    "Chikorita": {
        "tipo": "planta",
        "vida": 105,
        "habilidades": {
            "Látigo Cepa": {"tipo": "ataque", "poder": 35},
            "Danza Pétalo": {"tipo": "ataque", "poder": 30},
            "Regeneración": {"tipo": "pasiva", "dano": 0, "cura": 12, "duracion": 3}
        }
    },
    "Bellsprout": {
        "tipo": "planta",
        "vida": 95,
        "habilidades": {
            "Absorber": {"tipo": "ataque", "poder": 30},
            "Látigo Cepa": {"tipo": "ataque", "poder": 25},
            "Savia Vital": {"tipo": "pasiva", "dano": 0, "cura": 12, "duracion": 3}
        }
    }
}