from estudiante import Estudiante

estudiante1 = Estudiante("Juan", 15, "10mo")
estudiante1.imprimirDatos()
del estudiante1
print("Despues de del estudiante1")

estudiante2 = Estudiante.crearDesdeTexto("Maria,14,9no")
estudiante2.imprimirDatos()

Estudiante.mostrarCantidad()
print("Fin del programa")
