from estudiante import Estudiante

def main():
    nombre = input("Ingrese el nombre del estudiante: ")
    edad = int(input("Ingrese la edad del estudiante: "))
    grado = input("Ingrese el grado del estudiante: ")
    estudiante = Estudiante(nombre, edad, grado)
    while True:
        print("--- MENU ---")
        print("1. Ingresar datos")
        print("2. Imprimir datos")
        print("3. Matricular")
        print("4. Pagar pension")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            nombre = input("Ingrese el nombre del estudiante: ")
            edad = int(input("Ingrese la edad del estudiante: "))
            grado = input("Ingrese el grado del estudiante: ")
            estudiante.ingresarDatos(nombre, edad, grado)
        elif opcion == "2":
            estudiante.imprimirDatos()
        elif opcion == "3":
            estudiante.matricular()
        elif opcion == "4":
            estudiante.pagarPension()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion invalida")

main()
