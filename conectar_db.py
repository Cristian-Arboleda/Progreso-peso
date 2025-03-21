import psycopg2
import pandas as pd

host = 'dpg-cv3oekogph6c73esf4og-a.oregon-postgres.render.com'
database = 'progreso_peso_bd'
user = 'cristian'
password = 'GtCaKjh9HeVkb9NhDTYj73mGGYR0ZwIw'
port = '5432'

def conectar_db():
    conn = psycopg2.connect(
        host = host,
        database = database,
        user = user,
        password = password,
        port = port,
    )
    return conn


def credenciales_table():
    try:
        with conectar_db() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM credenciales"
                credenciales = pd.read_sql(query, conn)
                return credenciales
    except Exception as error:
        print(f'Error: {error}')

def consulta_db(query, obtener_datos = None):
    with conectar_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            if obtener_datos == 'todos':
                resultado = cur.fetchall()
                return resultado
            elif obtener_datos == 'uno':
                resultado = cur.fetchone()
                return resultado
            conn.commit()



if __name__ == '__main__':
    try:
        pass
    except Exception as error:
        print(f'Error: {error}')
