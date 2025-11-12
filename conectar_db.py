import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    
    conn = psycopg2.connect(
        host = HOST,
        database = DATABASE,
        user = USER,
        password = PASSWORD,
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