import psycopg2

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

def consulta_db(query, obtener_datos = None):
    with conectar_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            if obtener_datos == 'todos':
                return cur.fetchall()
            elif obtener_datos == 'uno':
                return cur.fetchone()
            conn.commit()

if __name__ == '__main__':
    pass