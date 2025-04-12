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
