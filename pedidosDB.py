import sqlite3 as sqlite

def criando_Tabela():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_Cliente TEXT NOT NULL,
                   tipo_Feijao TEXT,
                   tipo_Arroz TEXT,
                   macarrao TEXT,
                   verdura TEXT,
                   frango TEXT,
                   carne TEXT,
                   linguica TEXT,
                   obs TEXT,
                   preco FLOAT
                   )
               ''')
    conn.commit()
    conn.close()


def inserir(nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco):
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
                   INSERT INTO pedidos (nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco))
    conn.commit()
    conn.close()

def listar_Pedidos():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM pedidos order by id desc'
        )
    dados = cursor.fetchall()
    pedidos = []
    for dado in dados:
        pedidos.append(dado)
    conn.commit()
    conn.close()
    return pedidos



def id_buscar(pedido_id):
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id, ))
    pedido = cursor.fetchone()
    conn.close()
    return pedido



criando_Tabela()
