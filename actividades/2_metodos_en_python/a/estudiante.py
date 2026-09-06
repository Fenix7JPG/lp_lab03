class Estudiante():
    def __init__(self, nombre, edad, grado):
        self.nombre = nombre
        self.edad = edad
        self.grado = grado

    ###################### propiedad nombre ######################
    def getNombre(self):
        return self._nombre

    def setNombre(self, valor):
        if valor == "":
            self._nombre = "Sin nombre"
        else:
            self._nombre = valor

    nombre = property(getNombre, setNombre)
    ###################### fin propiedad ######################

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
