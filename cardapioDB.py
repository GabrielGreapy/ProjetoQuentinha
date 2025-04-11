import sqlite3 as sqlite

def criando_Tabela_Cardapio():
    conn = sqlite.connect('CardapioDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS cardapio (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cardapio TEXT NOT NULL,
                   data DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')
    conn.commit()
    conn.close()


def inserir_Cardapio( Cardapio):
    conn = sqlite.connect('CardapioDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO cardapio (cardapio)
                   VALUES ( ?)
                    ''', (Cardapio,))
    conn.commit()
    conn.close()


def ultimo_cardapio():
    conn = sqlite.connect('CardapioDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cardapio ORDER BY id DESC LIMIT 1
    ''')
    ultimo_cardapio = cursor.fetchone()
    conn.close()
    return ultimo_cardapio


criando_Tabela_Cardapio()