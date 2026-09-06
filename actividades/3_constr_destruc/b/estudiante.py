class Estudiante():
    def __init__(self, nombre, edad, grado):
        self.nombre = nombre
        self.edad = edad
        self.grado = grado
        Estudiante.cantidad = Estudiante.cantidad + 1

    def __new__(cls, *args):
        print("Ejecutando __new__: se crea la instancia antes de __init__")
        return super().__new__(cls)

    ###################### metodo __del__ ######################
    def __del__(self):
        print("Ejecutando __del__:", self.nombre, "se elimina")
    ###################### fin __del__ ######################

    def getNombre(self):
        return self._nombre

    def setNombre(self, valor):
        if valor == "":
            self._nombre = "Sin nombre"
        else:
            self._nombre = valor

    nombre = property(getNombre, setNombre)

    colegio = "UCSM"
    cantidad = 0

    @classmethod
    def crearDesdeTexto(cls, texto):
        partes = texto.split(",")
        return cls(partes[0], int(partes[1]), partes[2])

    @classmethod
    def mostrarCantidad(cls):
        print("Cantidad de estudiantes creados:", cls.cantidad)

    @staticmethod
    def validarEdad(edad):
        if edad > 0 and edad < 100:
            return True
        return False

    @staticmethod
    def convertirMayusculas(texto):
        return texto.upper()

    def ingresarDatos(self, nombre, edad, grado):
        self.nombre = nombre
        self.edad = edad
        self.grado = grado

    def imprimirDatos(self):
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Grado:", self.grado)

    def matricular(self):
        print(self.nombre, "ha sido matriculado en el grado", self.grado)

    def pagarPension(self):
        print(self.nombre, "ha pagado la pension correspondiente al grado", self.grado)
