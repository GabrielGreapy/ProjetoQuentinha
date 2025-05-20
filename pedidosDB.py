import sqlite3 as sqlite


def criando_Tabela():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     id_Cliente INTEGER,
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
                     hora_Do_Pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
                     status_Pedido TEXT NOT NULL,
                     forma_Pagamento TEXT NOT NULL
                )
                ''')
    conn.commit()
    conn.close()




def inserir(id_Cliente ,nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega, forma_Pagamento):
    status_Pedido = "Não Entregue"
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
                   INSERT INTO pedidos (id_Cliente, nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega, forma_Pagamento, status_Pedido) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (id_Cliente ,nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verdura, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega, forma_Pagamento, status_Pedido))
    conn.commit()
    conn.close()


def retirar(id):
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE FROM pedidos WHERE id = ?
                    ''', (id,))
    conn.commit()
    conn.close()

def entregue(id):
    status = "Entregue"
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    UPDATE pedidos
                    SET status_Pedido = ?
                    WHERE id = ?
                    ''', (status, id))
    conn.commit()
    conn.close()


def listar_Pedidos():
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM pedidos WHERE status_Pedido = "Não Entregue"
            ORDER BY id DESC'''
        )
    dados = cursor.fetchall()
    pedidos = []
    for dado in dados:
        pedidos.append(dado)
    conn.commit()
    conn.close()
    return pedidos


def listar_Pedidos_Historico():
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

def pedidosDeCliente(id):
    conn = sqlite.connect('pedidosDB.sqlite')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM pedidos WHERE id_Cliente = ? AND status_Pedido = "Não Entregue"
                   ''', (id, ))
    dados = cursor.fetchall()
    conn.close()
    pedidos = [dict(dado) for dado in dados]
    return pedidos

def pedidosDeClienteHistorico(id):
    conn = sqlite.connect('pedidosDB.sqlite')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM pedidos WHERE id_Cliente = ?''', (id, ))
    dados = cursor.fetchall()
    conn.close()
    pedidos = [dict(dado) for dado in dados]
    return pedidos

def canceladoCliente(id):
    status = "Cancelado por Cliente"
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    UPDATE pedidos
                    SET status_Pedido = ?
                    WHERE id = ?
                    ''', (status, id,))
    conn.commit()
    conn.close()


def editarPedido(tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica,
                    obs, horario_Entrega, local_Entrega, preco, pagamento, id):
    
    conn = sqlite.connect('pedidosDB.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    UPDATE pedidos
                    SET tipo_Feijao = ?, tipo_Arroz = ?, macarrao = ?, verdura = ?, frango = ?, carne = ?, linguica=?,
                        obs = ?, horario_Entrega = ?, local_Entrega = ?, preco = ?, forma_Pagamento = ?
                    WHERE id = ?
                    ''', (tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica,
                    obs, horario_Entrega, local_Entrega, preco, pagamento,id))
    conn.commit()
    conn.close()

criando_Tabela()