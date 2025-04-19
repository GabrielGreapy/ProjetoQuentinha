import sqlite3 as sqlite


def criando_Tabela_Devedores():
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS devedores(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_Cliente TEXT NOT NULL
                )
                ''')
    conn.commit()
    conn.close()


def inserir_Devedor(nome_Cliente):
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO devedores(nome_Cliente)
                   VALUES( ?)
                   ''',(nome_Cliente,)
                    )
    conn.commit()
    conn.close()



def listar_Devedores():
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM devedores ORDER BY id DESC'''
        )
    dados = cursor.fetchall()
    contas = []
    for dado in dados:
        contas.append(dado)
    conn.commit()
    conn.close()
    return contas




def pegar_Devedor(id_conta):
    conn = sqlite.connect('dividasDB.sqlite')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM devedores WHERE id = ?''', (id_conta,)
    )
    conta = cursor.fetchone()
    conn.close()
    return dict(conta) if conta else None


def Gabriel3(nome_Cliente):
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO devedores( nome_Cliente)
        VALUES( ?)
        ''', ( nome_Cliente,))
    conn.commit()
    conn.close()




def criando_Tabela_Dividas():
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS dividas (
                   id_Divida INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_Cliente TEXT NOT NULL,
                   id_devedor INT NOT NULL,
                   valor REAL NOT NULL
                )
                ''')
    conn.commit()
    conn.close()


def inserir_Divida(id, nome_Cliente, valor):
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO dividas( nome_Cliente, id_Devedor, valor)
                   VALUES ( ?, ?, ?)

                   ''', ( id, nome_Cliente, valor))
    conn.commit()
    conn.close()


def listar_Dividas():
    conn = sqlite.connect('dividasDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM dividas ORDER BY id_Divida DESC'''
        )
    dados = cursor.fetchall()
    dividas = []
    for dado in dados:
        dividas.append(dado)
    conn.commit()
    conn.close()
    return dividas


def pegar_Dividas(id_conta):
    conn = sqlite.connect('dividasDB.sqlite')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM dividas WHERE id_Devedor = ?''', (id_conta,)
    )
    dados = cursor.fetchall()
    dividas = []
    for dado in dados:
        dividas.append(dado) 
    conn.close()
    return dividas if dividas else None


def pegar_Divida(id_divida):
    conn = sqlite.connect('dividasDB.sqlite')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM dividas WHERE id_Divida = ?''', (id_divida,)
    )
    dividas = cursor.fetchone() 
    conn.close()
    return dividas if dividas else None

criando_Tabela_Dividas()
criando_Tabela_Devedores()
# Gabriel3("Gabriel")
# inserir_Divida( "Gabriel", "1", "12,00")