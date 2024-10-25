# database.py
import sqlite3

def criar_conexao(db_file):
    """Cria uma conexão com o banco de dados SQLite especificado."""
    conexao = sqlite3.connect(db_file)
    return conexao

def criar_tabelas(conexao):
    """Cria as tabelas no banco de dados, caso não existam."""
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abertura REAL NOT NULL,
            fechamento REAL,
            data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_fechamento DATETIME
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_total REAL NOT NULL,
            data_venda TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')

    conexao.commit()
