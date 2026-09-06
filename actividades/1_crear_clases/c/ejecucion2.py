from estudiante import Estudiante

estudiante1 = Estudiante("Ana", 14, "3ro")
estudiante2 = Estudiante("Beto", 15, "4to")
estudiante3 = Estudiante("Carla", 16, "5to")
estudiantes = [estudiante1, estudiante2, estudiante3]

for estudiante in estudiantes:
    estudiante.imprimirDatos()
    estudiante.matricular()
    estudiante.pagarPension()
    print("")
