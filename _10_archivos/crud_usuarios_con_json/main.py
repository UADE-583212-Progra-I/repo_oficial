import src.services as services
import src.interface as interface

def main():
    while True:
        print("\n  --- Gestión de Usuarios ---")
        print("  1. Crear usuario")
        print("  2. Ver usuarios")
        print("  3. Ver usuario por ID")
        print("  0. Salir")

        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            ok = services.crear_usuario()
            print("Usuario guardado en data/usuarios.json" if ok else "No se pudo crear el usuario.")
        elif opcion == "2":
            usuarios = services.listar_usuarios()   # levanta el JSON
            interface.mostrar_usuarios(usuarios)
        elif opcion == "3":
            usuario = services.buscar_usuario_por_id()
            print(usuario) if usuario else print("ID no encontrado")
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# ============================================================
if __name__ == "__main__":
    main()
