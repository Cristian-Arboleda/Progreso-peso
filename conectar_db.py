import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    PGHOST = os.getenv('HOST')
    PGDATABASE = os.getenv('DATABASE')
    PGUSER = os.getenv('USER')
    PGPASSWORD = os.getenv('PASSWORD')
    
    conn = psycopg2.connect(
        host = PGHOST,
        database = PGDATABASE,
        user = PGUSER,
        password = PGPASSWORD,
        sslmode="require",
    )
    return conn

def consulta_db(query, obtener_datos = None):
    with conectar_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            if obtener_datos == 'todos':
                return cur.fetchall()
            elif obtener_datos == 'uno':
                return cur.fetchone()
            conn.commit()


'''
CREATE TABLE progreso_peso_valentina(
	id INTEGER,
	fecha DATE,
	diurno numeric(6,3),
	nocturno numeric(6,3)
)
'''
if __name__ == '__main__':
    conn = conectar_db()