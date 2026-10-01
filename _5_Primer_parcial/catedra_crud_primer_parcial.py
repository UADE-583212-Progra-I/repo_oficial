# ============================================================
# DATOS INICIALES
# ============================================================

# ── Registro user admin
USER_ADMIN = {
        "id_user": 1,
        "username": "admin",
        "password": "Uade*2026",
        "email": "admin@uade.edu.ar",
        "cell": 1133445566,
        "id_role": 1,
    }

# ── Entidad: usuarios (se gestiona con CRUD) ─
users = [USER_ADMIN]

# ── Entidad: roles (solo lo gestiona el admin)
ROLE_ADMIN = {"id_role": 1, "role_name": "admin"}
ROLE_USER = {"id_role": 2, "role_name": "user"}
roles = [ROLE_ADMIN, ROLE_USER]



# ============================================================
# UTILIDADES GENERALES
# ============================================================

def validar_password(password):
    # 8 caracteres de minimo: longitud
    # 1 mayuscula: mayuscula
    # 1 minuscula: minuscula
    # al menos 3 numeros: numero
    length = len(password) >= 8
    n_upper = n_lower = n_digit = 0
    
    for c in password:
        if c.isupper():
            n_upper += 1
        elif c.islower():
            n_lower += 1
        elif c.isdigit():
            n_digit += 1
            
    upper = n_upper > 0
    lower = n_lower > 0
    number = n_digit > 3
    
    return length and number and upper and lower

def validar_id_role(id_role):
    ids = [role["id_role"] for role in roles]
    return id_role in ids

def gen_id_usuario():
    ids = [user["id_user"] for user in users]
    return max(ids)+1

def buscar_role_por_id(id_role):
    for role in roles:
        if role["id_role"] == id_role:
            return role["role_name"]
    return None

def buscar_user_por_id(id_user):
    for user in users:
        if user["id_user"] == id_user:
            return user
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

    # Construir el diccionario del usuario
    nuevo_usuario = {
        "id_user": id_user,
        "username": username,
        "password": password,
        "email": email,
        "id_role": id_role,
    }

    users.append(nuevo_usuario)
    print("Usuario agregado exitosamente!")


def mostrar_usuarios():
    print("\n--- Usuarios registrados ---")
    for user in users:
        print(f"usernane: {user["username"]}")
        print(f"password: {enmascarar(user["password"])}")
        print(f"email: {user["email"]}")
        print(f"role: {buscar_role_por_id(user["id_role"])}")

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
        print("  0. Volver")

        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
