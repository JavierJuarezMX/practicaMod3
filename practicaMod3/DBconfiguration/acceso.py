import psycopg2
import getpass

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = "Admin"
DB_PASSWORD = "p4ssw0rdDB"

def conectar_db():
    try:
        conn = psycopg2.connect(
            host = DB_HOST,
            port = DB_PORT,
            database = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD
        )
        return conn

    except Exception as e:
        print("Error de conexión.", e)
        return None
    
def obtener_datos_usuario(username, password):
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
        else:
            print("\nUsuario o contraseña incorrectos.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error de consulta a la base de datos: ",e)

def insertar_usuario(nombre, correo,telefono, fecha_nacimiento, username, password):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # Insertar en la tabla usuarios
        cursor.execute(
            """
            INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
            VALUES (%s, %s, %s, %s) RETURNING id_usuario;
            """, (nombre, correo, telefono, fecha_nacimiento)
        )

        id_usuario = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT INTO credenciales (id_usuario, username, password_hash)
            VALUES (%s, %s, %s);
            """, (id_usuario, username, password)
        )

        conn.commit()
        print("Nuevo usuario insertado correctamente.")

    except Exception as e:
        print("Error al insertar el nuevo usuario: ", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Inicio de sesión en la base de datos.")

    username = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")
    
    obtener_datos_usuario(username, password)

    #print("Insertar nuevo usuario")
    #nombre = input("Ingrese el nombre del nuevo usuario: ")
    #correo = input("Ingrese el correo del nuevo usuario: ")
    #telefono = input("Ingrese el teléfono del nuevo usuario: ")
    #fecha_nacimiento = input("Ingrese la fecha de nacimiento del nuevo usuario (YYYY-MM-DD): ")
    #username = input("Ingrese el nombre de usuario para el nuevo usuario: ")
    #password = input("Ingrese la contraseña para el nuevo usuario: ")
    #insertar_usuario(nombre, correo, telefono, fecha_nacimiento, username, password)