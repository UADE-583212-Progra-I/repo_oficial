from Primer_parcial.estudiante_matrices_primer_parcial import procesar_digito_9
# ============================================================
# DATOS INICIALES
# ============================================================

# ── Entidad: roles (hardcoded)
ROLE_ADMIN =
ROLE_USER = 
roles = 

# ============================================================
# UTILIDADES GENERALES
# ============================================================

def validar_password(password):
    length = True if len(password) >= 8 else False
    n_upper = n_lower = n_digit = 0
    # Completar...
    
    return length and number and upper and lower

def buscar_role_por_id(id_role):
    for i in range(roles):
        if roles[i][0] == id_role:
            return roles[i][1]
    return None

def enmascarar(password):
    return password[:-3] + "***"

# ============================================================
# CRUD DE USUARIOS
# ============================================================

def crear_usuario():
    id_user = gen_id_usuario()
    username = input("Ingrese su username: ").strip()
    password = input("Ingrese su password: ").strip()
    while not validar_password(password):
        print("Su password no cumple con los requerimientos. Intente nuevamente...")
        password = input("Ingrese su password: ").strip()
    email = input("Ingrese su email: ").strip()
    id_role = int(input("Ingrese el id_role: ").strip())
    while not validar_id_role(id_role):
        print("El id_role ingresado en inválido. Intente nuevamente...")
        id_role = int(input("Ingrese el id_role: ").strip())

    # Construye el diccionario user
    # Inserta el diccionario user a la lista global users

    print("Usuario agregado exitosamente!")


def mostrar_usuarios():
    print("\n--- Usuarios registrados ---")
    # Encabezados - Header
    print(f"Usernane | Password | Email | Role")
    # Iterar la lista users
    # username e email se muestran sin transformaciones
    # password se enmascara con enmascarar(password)
    # role_name se obtiene con buscar_role_por_id(id_role)


def eliminar_usuario():
    print("\n--- Eliminar usuario ---")
    id_user = int(input("ID del usuario a eliminar: "))
    user = buscar_user_por_id(id_user)
    if not user:
        print(f"No se encontró ningún usuario con id {id_user}.")
        return
    users.remove(user)
    print(f"Usuario eliminado correctamente.")


def main():
    """Función principal con menú interactivo."""
    while True:
        print("\n  --- Gestión de Usuarios ---")
        print("  1. Crear usuario")
        print("  2. Ver usuarios")
        print("  3. Eliminar usuario")
        print("  4. Procesar Dígito 9")
        print("  0. Volver")

        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "4":
            procesar_digito_9()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
