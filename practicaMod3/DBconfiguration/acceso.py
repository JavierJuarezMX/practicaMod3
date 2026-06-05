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

if __name__ == "__main__":
    print("Inicio de sesión en la base de datos.")

    username = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")
    
    obtener_datos_usuario(username, password)