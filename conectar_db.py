import psycopg2

host = 'ep-bold-fire-a56towq6-pooler.us-east-2.aws.neon.tech'
database = 'progreso-peso-bd'
user = 'neondb_owner'
password = 'npg_XwISfjxY0rt5'
port = '5432'

def conectar_db():
    conn = psycopg2.connect(
        host = host,
        database = database,
        user = user,
        password = password,
        port = port,
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
	diurno INTEGER,
	nocturno INTEGER
)
'''
if __name__ == '__main__':
    conn = conectar_db()