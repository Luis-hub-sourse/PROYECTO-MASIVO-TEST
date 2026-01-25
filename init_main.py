from PyQt5 import QtWidgets
import sys
from pruebas.test_ventana_usuarios import VentanaUsuarios
from ventanas.ventana_principal import VentanaPrincipal as Vet
from main import VentanaPrincipal

def main():
    print("Iniciando la aplicación...")
    print("Que programa desea ejecutar?")
    print("1. Ventana Principal")
    print("2. Test Ventana")

    opcion = input("Ingrese 1 o 2: ")

    if opcion == "1":
        app = QtWidgets.QApplication(sys.argv)
        ventana = Vet()
        ventana.show()
        sys.exit(app.exec_())
    elif opcion == "2":
        app = QtWidgets.QApplication(sys.argv)
        ventana_test = VentanaUsuarios()
        ventana_test.show()
        sys.exit(app.exec_())
    elif opcion == "3":
        app = QtWidgets.QApplication(sys.argv)
        ventana_test = VentanaPrincipal()
        ventana_test.show()
        sys.exit(app.exec_())
    else:
        print("Opción no válida. Saliendo de la aplicación.")

if __name__ == "__main__":
    main()