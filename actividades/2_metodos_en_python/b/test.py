from estudiante import Estudiante

estudiante1 = Estudiante("Juan", 15, "10mo")
estudiante1.imprimirDatos()

estudiante2 = Estudiante.crearDesdeTexto("Maria,14,9no")
estudiante2.imprimirDatos()
estudiante2.matricular()
estudiante2.pagarPension()

Estudiante.mostrarCantidad()
print("Colegio:", Estudiante.colegio)
