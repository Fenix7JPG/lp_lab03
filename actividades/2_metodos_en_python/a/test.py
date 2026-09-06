from estudiante import Estudiante

estudiante1 = Estudiante("Juan", 15, "10mo")
estudiante1.imprimirDatos()

estudiante1.nombre = "Juan Perez"
print("Nombre modificado con property:", estudiante1.nombre)

estudiante1.nombre = ""
print("Nombre con valor invalido:", estudiante1.nombre)

estudiante1.ingresarDatos("Maria", 14, "9no")
estudiante1.matricular()
estudiante1.pagarPension()
