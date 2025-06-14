import sqlite3 as sqlite

def criando_Tabela_Administracao():
    conn = sqlite.connect('administracaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                   id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_Funcionario TEXT NOT NULL,
                   email_Funcionario TEXT NOT NULL,
                   senha_Funcionario TEXT NOT NULL
                )
                ''')
    conn.commit()
    conn.close()





def criando_Tabela_Clientes():
    conn = sqlite.connect('administracaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                   id_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_Cliente TEXT NOT NULL,
                   email_Cliente TEXT NOT NULL,
                   senha_Cliente TEXT NOT NULL,
                   numero_Cliente TEXT
                )
                ''')
    conn.commit()
    conn.close()


def inserir_Cliente( email, nome , numero, senha):
    conn = sqlite.connect('administracaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO clientes ( nome_Cliente, email_Cliente, numero_Cliente, senha_Cliente)
                   VALUES ( ?, ?, ?, ?)
                    ''', (nome, email, numero, senha))
    conn.commit()
    conn.close()


def inserir_Funcionario(nome_Funcionario, email_Funcionario, senha_Funcionario):
    conn = sqlite.connect('administracaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO funcionarios ( email_Funcionario, nome_Funcionario, senha_Funcionario)
                   VALUES ( ?, ?, ? )
                   ''', ( email_Funcionario, nome_Funcionario, senha_Funcionario))
    conn.commit()
    conn.close()





def pegar_Clientes(email, senha):
    conn = sqlite.connect('administracaoDB.sqlite')
    conn.row_factory = sqlite.Row 
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clientes
        WHERE email_Cliente = ? 
        AND senha_Cliente = ?
        ''',(email, senha))
    clientes = cursor.fetchone()
    conn.close()
    return dict(clientes) if clientes else None


def conta_Indivindual(email, senha):
    conn = sqlite.connect('administracaoDB.sqlite')
    conn.row_factory = sqlite.Row 
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clientes
        WHERE email_Cliente = ? 
        AND senha_Cliente = ?
        ''',(email, senha))
    clientes = cursor.fetchone()
    conn.close()
    return dict(clientes) if clientes else None



def pegar_Funcionarios(email, senha):
    conn = sqlite.connect('administracaoDB.sqlite')
    conn.row_factory = sqlite.Row 
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM funcionarios
        WHERE email_Funcionario = ? 
        AND senha_funcionario = ?
        ''',(email, senha))
    funcionarios = cursor.fetchone()
    conn.close()
    return dict(funcionarios) if funcionarios else None



def inserir_admin_padrao():
    try:
        conn = sqlite.connect('administracaoDB.sqlite')  
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM funcionarios")
        total = cursor.fetchone()[0]

        if total == 0:
            inserir_Funcionario( "Admin", "admin@silvania.com", "silvaniaDelicias167" )
                
            print("Funcionário admin padrão inserido.")
        else:
            print("Funcionário já existente, nenhum admin padrão inserido.")

        conn.commit()
    except Exception as e:
        print("Erro ao verificar ou inserir admin padrão:", e)
    finally:
        conn.close()


criando_Tabela_Administracao()
criando_Tabela_Clientes()
inserir_admin_padrao()

