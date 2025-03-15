import psycopg2
import pandas as pd

host = 'dpg-cv3oekogph6c73esf4og-a.oregon-postgres.render.com'
database = 'progreso_peso_bd'
user = 'cristian'
password = 'GtCaKjh9HeVkb9NhDTYj73mGGYR0ZwIw'
port = '5432'

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(
            host = host,
            database = database,
            user = user,
            password = password,
            port = port,
        )
        # Crear tabla credenciales
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS credenciales(
                usuario VARCHAR(45) NOT NULL, 
                password VARCHAR(45) NOT NULL
            )
        """)
        conn.commit()
        
        # Insertar datos en la tabla credenciales
        #cur.execute("INSERT INTO credenciales(usuario, password) VALUES('valentina', '111')")
        
        # eliminar datos
        #cur.execute("DELETE FROM credenciales WHERE usuario = 'pepito'")
        
        # Mostrar tabla
        cur.execute("SELECT * FROM credenciales")
        tabla = cur.fetchall()
        conn.commit()
        
        # pandas
        query = 'SELECT * FROM credenciales'
        datos = pd.read_sql(query, conn)
        
    except Exception as error:
        print('Error:', error)
    

def credenciales_table():
    conn = None
    try:
        conn = psycopg2.connect(
            host = host,
            database = database,
            user = user,
            password = password,
            port = port,
        )
        
        query = "SELECT * FROM credenciales"
        
        credenciales = pd.read_sql(query, conn)
        
        print('correct connetion')
    except Exception as error:
        print(f'Error: {error}')
    finally:
        if not conn == None:
            conn.close()
    return credenciales