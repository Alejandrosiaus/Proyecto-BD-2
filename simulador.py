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

