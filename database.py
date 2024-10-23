import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('database_hortifruti-py.db')
        print("Conexão ao banco de dados estabelecida com sucesso.")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
