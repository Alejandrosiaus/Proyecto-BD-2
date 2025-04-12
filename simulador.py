import threading
import time
import psycopg2

# Configuración de conexión
DB_CONFIG = {
    'dbname': 'reserva_eventos',
    'user': 'postgres',
    'password': 'P101104e',
    'host': 'localhost',
    'port': 5432
}

ASIENTO_ID = 7
NIVEL_AISLAMIENTO = 'SERIALIZABLE'
RESERVAS_EXITOSAS = 0
RESERVAS_FALLIDAS = 0
lock = threading.Lock()

def reservar_asiento(usuario_id):
    global RESERVAS_EXITOSAS, RESERVAS_FALLIDAS
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_session(isolation_level=NIVEL_AISLAMIENTO)
        cur = conn.cursor()

        cur.execute("BEGIN;")

        cur.execute("SELECT * FROM reserva WHERE id_asiento = %s FOR UPDATE;", (ASIENTO_ID,))
        if cur.fetchone():
            with lock:
                RESERVAS_FALLIDAS += 1
            conn.rollback()
            print(f"Usuario {usuario_id}: El asiento ya está reservado (SELECT)")
        else:
            try:
                cur.execute("INSERT INTO reserva (id_usuario, id_asiento) VALUES (%s, %s);", (usuario_id, ASIENTO_ID))
                conn.commit()
                with lock:
                    RESERVAS_EXITOSAS += 1
                print(f"Usuario {usuario_id}: ¡Reserva exitosa!")
            except psycopg2.Error as insert_error:
                conn.rollback()
                with lock:
                    RESERVAS_FALLIDAS += 1
                print(f"Usuario {usuario_id}: Error al insertar -> {insert_error.pgerror}")

        cur.close()
        conn.close()
    except Exception as e:
        with lock:
            RESERVAS_FALLIDAS += 1
        print(f"Usuario {usuario_id}: Error general -> {e}")
        
def simular_concurrencia(cantidad_usuarios):
    global RESERVAS_EXITOSAS, RESERVAS_FALLIDAS
    RESERVAS_EXITOSAS = 0
    RESERVAS_FALLIDAS = 0

    hilos = []
    inicio = time.time()
    for i in range(cantidad_usuarios):
        hilo = threading.Thread(target=reservar_asiento, args=(i+1,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()
    fin = time.time()

    tiempo_ms = round((fin - inicio)*1000, 2)

    print("\n--- RESULTADOS ---")
    print(f"Usuarios: {cantidad_usuarios}")
    print(f"Nivel de aislamiento: {NIVEL_AISLAMIENTO}")
    print(f"Reservas exitosas: {RESERVAS_EXITOSAS}")
    print(f"Reservas fallidas: {RESERVAS_FALLIDAS}")
    print(f"Tiempo total: {tiempo_ms} ms")
    print("------------------\n")

if _name_ == "_main_":
    simular_concurrencia(30)
