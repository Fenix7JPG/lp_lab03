from estudiante import Estudiante

estudiante = Estudiante("Ana", 14, "3ro")

print("Validar edad 14:", Estudiante.validarEdad(14))
print("Validar edad -5:", Estudiante.validarEdad(-5))
print("Nombre en mayusculas:", Estudiante.convertirMayusculas(estudiante.nombre))

estudiante.imprimirDatos()
estudiante.matricular()
estudiante.pagarPension()
