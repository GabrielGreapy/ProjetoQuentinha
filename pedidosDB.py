import sqlite3 as sqlite


def criando_Tabela():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     id_Cliente INTEGER NOT NULL,
                     nome_Cliente TEXT NOT NULL,
                     tipo_Feijao TEXT,
                     tipo_Arroz TEXT,
                     macarrao TEXT,
                     verdura TEXT,
                     frango TEXT,
                     carne TEXT,
                     linguica TEXT,
                     obs TEXT,
                     preco REAL,
                     horario_Entrega DATETIME,
                     local_Entrega TEXT NOT NULL,
                     hora_Do_Pedido DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')
    conn.commit()
    conn.close()




def inserir(id_Cliente ,nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega):
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
                   INSERT INTO pedidos (id_Cliente, nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (id_Cliente ,nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega))
    conn.commit()
    conn.close()


def retirar(id):
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE pedidos WHERE id = ?
                    ''', (id))
    conn.commit()
    conn.close()


def listar_Pedidos():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM pedidos order by id desc'''
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