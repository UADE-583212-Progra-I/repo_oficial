import src.services as services
import src.interface as interface

def main():
    while True:
        print("\n  --- Gestión de Usuarios ---")
        print("  1. Crear usuario")
        print("  2. Ver usuarios")
        print("  3. Buscar usuario por ID")
        print("  0. Salir")

        opcion = input("\n  Opción: ").strip()
        match(opcion):
            case "1":
                # 1. Crear usuario
                nuevo_usuarios = interface.get_nuevo_usuario()
                ok = services.crear_usuario(nuevo_usuarios)
                print("Usuario guardado en data/usuarios.json" if ok else "No se pudo crear el usuario.")
            case "2":
                # 2. Ver usuarios
                usuarios = services.listar_usuarios()   # levanta el JSON
                interface.mostrar_usuarios(usuarios)
            case "3":
                # 3. Buscar usuario por ID
                id_usuario = interface.get_id_usuario()
                usuario = services.buscar_usuario_por_id(id_usuario)
                if usuario:
                    interface.mostrar_usuarios([usuario])
                else:
                    interface.mostrar_warning("ID no encontrado")
            case "0":
                break
            case _:
                print("Opción inválida.")


# ============================================================
if __name__ == "__main__":
    main()
