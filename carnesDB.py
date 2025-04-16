import sqlite3 as sqlite


def criando_Tabela_Carnes():
    conn = sqlite.connect('mantimentosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS carnes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   carne INTEGER NOT NULL,
                   linguica INTEGER NOT NULL,
                   frango INTEGER NOT NULL,
                   data DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')
    conn.commit()
    conn.close()


def inserir_Carnes(carne, linguica, frango):
    conn = sqlite.connect('mantimentosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO carnes (carne, linguica, frango)
                   VALUES (?, ?, ?)
                    ''', (carne, linguica, frango))
    conn.commit()
    conn.close()


def info_Estoque():
    conn = sqlite.connect('mantimentosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(''' 
                    SELECT * FROM carnes ORDER BY id DESC LIMIT 1
    ''')
    carnes_do_dia = cursor.fetchone()
    conn.close()

    
    if carnes_do_dia:
        return {
            'id': carnes_do_dia[0],
            'carne': int(carnes_do_dia[1]) if carnes_do_dia[1] else 0,
            'linguica': int(carnes_do_dia[2]) if carnes_do_dia[2] else 0,
            'frango': int(carnes_do_dia[3]) if carnes_do_dia[3] else 0,
            'data': carnes_do_dia[4]
        }
    else:
        return {
            'id': None,
            'carne': 0,
            'linguica': 0,
            'frango': 0,
            'data': None
        }


def modificar_Estoque(mod_Carne, mod_Linguica, mod_Frango):
    carnes_Do_Dia = info_Estoque()
    
    if carnes_Do_Dia['id'] is None:
        print("Erro: Nenhum dado encontrado para o estoque.")
        return

    
    id = carnes_Do_Dia['id']
    carne = carnes_Do_Dia['carne']
    if carne < 0:
        carne -= mod_Carne
    else:
        carne += mod_Carne
    linguica = carnes_Do_Dia['linguica']
    if linguica < 0:
        linguica -= mod_Linguica
    else: 
        linguica += mod_Linguica
    frango = carnes_Do_Dia['frango'] + mod_Frango
    if frango < 0:
        frango -= mod_Frango
    else:
        frango += mod_Frango
    conn = sqlite.connect('mantimentosDB.sqlite')
    cursor = conn.cursor()
    cursor.execute(''' 
                    UPDATE carnes
                    SET carne = ?, linguica = ?, frango = ?
                    WHERE id = ?
    ''', (carne, linguica, frango, id))
    conn.commit()  
    conn.close()
    print(f"Estoque atualizado: Carne={carne}, Linguica={linguica}, Frango={frango}")



criando_Tabela_Carnes()
