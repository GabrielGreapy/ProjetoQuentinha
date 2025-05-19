from flask import *
from dotenv import load_dotenv
import os
app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

import pedidosDB
import administracaoDB
import cardapioDB
import carnesDB
import dividasDB



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pedindo", methods=('POST', 'GET'))
def pedindo():
    mensagem = []
    if request.method == 'POST':
        try:
            nome_Cliente = session['nome_Cliente']
        except:
            mensagem.append("Algo deu errado no nome do cliente")
        try:
            id_Cliente = session['id_Cliente']
        except:
            mensagem.append("Algo deu errado com o id do Cliente")

        tipo_Feijao = request.form.get('tipo_Feijao', '')
        tipo_Arroz = request.form.get('tipo_Arroz', '')
            
            
        opcionais = request.form.getlist('opcionais')  
        carnes = request.form.getlist('carnes')        
        try:
            local_Entrega = request.form.get('local_Entrega', '').strip()
        except:
            mensagem.append("Algo deu errado no local de entrega")
        if not local_Entrega:
            local_Entrega = 'Buscará no estabelecimento'
        preco = 12 + 2 * sum(carne in carnes for carne in["Carne", "Frango", "Linguiça"])
        macarrao = "Sim" if "Macarrão" in opcionais else "Não"
        verduras = "Sim" if "Verduras" in opcionais else "Não"
        carne    = "Sim" if "Carne" in carnes else "Não"
        frango   = "Sim" if "Frango" in carnes else "Não"
        linguica = "Sim" if "Linguiça" in carnes else "Não"
        try:
            horario_Entrega = request.form.get('horario_Entrega', '').strip()
        except:
            mensagem.append('Algo deu errado no horario de entrega')
        obs = request.form.get('obs', '')
        pagamento = request.form.get("pagamento", "").strip()
        try:
            pedidosDB.inserir(id_Cliente, nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega, pagamento)
            return redirect(url_for("cliente_Perfil", id=session['id_Cliente']))
        except:
            mensagem.append("Algo deu errado na hora de enviar o pedido.")
            
        
    return render_template("pedindo_Quentinha.html", mensagem=mensagem)


@app.route("/lista")
def lista():
    if 'funcionario_nome' in session:
        pedidos= pedidosDB.listar_Pedidos()
        return render_template("lista_pedidos.html", pedidos=pedidos)



@app.route("/lista/<int:pedido_id>")
def pedido_completo(pedido_id):
    pedido = pedidosDB.id_buscar(pedido_id)
    if pedido:
        return render_template("pedido_completo.html", pedido=pedido)
    else: 
        mensagem='Pedido não encontrado'
        return render_template("lista_pedido.html", mensagem=mensagem)


@app.route("/login_funcionario", methods=( 'POST', 'GET'))
def login_Funcionario():
    mensagem = []
    if request.method == 'POST':
        try: 
            nome = request.form.get('email', '').strip()
        except:
            mensagem.append("Algo errado com o email")
        try:
            senha = request.form.get('senha', '').strip()
        except:
            mensagem.append("Algo deu errado com a senha")
        try:
            if nome and senha:
                funcionario = administracaoDB.pegar_Funcionarios(nome, senha)
                if funcionario:
                    session['funcionario_id'] = funcionario['id_funcionario']
                    session['funcionario_nome'] = funcionario['nome_Funcionario']
                    return redirect(url_for('funcionario'))
                else: mensagem= 'Funcionário não existe.' 
            else: mensagem.append('Escreva algo nos campos')
        except: 
            mensagem.append('Algo deu errado no login')
    return render_template("login_funcionario.html", mensagem = mensagem)
    

@app.route("/funcionario")
def funcionario():
    if 'funcionario_nome' in session:
        nome = session['funcionario_nome']
        return render_template("funcionario.html", nome=nome)
    else: 
        return redirect(url_for("login_Funcionario"))

@app.route("/login_cliente", methods=("POST", "GET"))
def login_cliente():
    mensagem = []
    if request.method == "POST":
        try:
            nome = request.form.get('email', '').strip()
        except:
            mensagem.append("Algo deu errado com o nome")
        try:
            senha = request.form.get('senha', '').strip()
        except:
            mensagem.append("Algo deu errado com a senha")
        try:
            if nome and senha:
                cliente = administracaoDB.pegar_Clientes(nome, senha)
                try:
                    session['nome_Cliente'] = cliente['nome_Cliente']
                    session['numero_Cliente'] = cliente['numero_Cliente']
                    session['id_Cliente'] = cliente['id_Cliente']
                    return redirect(url_for("cliente_Perfil", id=session['id_Cliente']))
                except: 
                    mensagem.append("Cliente não existe")
            else: 
                mensagem.append('Preencha as informações')
        except:
            mensagem.append = ("Algo deu errado no login")
    return render_template("login_cliente.html", mensagem=mensagem)


@app.route("/cliente_Perfil/<int:id>")
def cliente_Perfil(id):
    if 'nome_Cliente' in session:
        id = id
        nome = session['nome_Cliente']
        numero = session['numero_Cliente']
        pedidos = pedidosDB.pedidosDeCliente(id)
        return render_template("cliente_Perfil.html", nome=nome , numero=numero, pedidos=pedidos, id=id)
    else: return redirect(url_for("/login_cliente"))


@app.route("/criar_Cliente", methods=( "POST", "GET"))
def criar_Cliente():
    mensagem = []
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
        except:
            mensagem.append('Algo deu errado no email')
        try:
            nome = request.form.get("nome", "").strip()
        except:
            mensagem.append('Algo deu errado no nome')
        try:
            numero = request.form.get("numero", "").strip()
        except:
            mensagem.append('Algo deu errado no numero')
        try:
            senha = request.form.get("senha", "").strip()
        except:
            mensagem.append("Algo deu errado na senha")
        try:
            if nome and numero and senha and email:
                administracaoDB.inserir_Cliente( email, nome, numero, senha)
                return redirect(url_for("login_cliente"))
            else:
                mensagem.append("Alguns dos campos está faltando")
        except:
            mensagem.append("Algo deu errado na criação de cliente.")
    return render_template("criar_Cliente.html")

@app.route("/criar_Funcionario", methods=('POST', 'GET'))
def criar_Funcionario():
    if 'funcionario_nome' in session:
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            nome = request.form.get("nome", "").strip()
            senha = request.form.get("senha", "").strip()
            administracaoDB.inserir_Funcionario(nome, email, senha)
        return render_template("criar_Funcionario.html")
    else: return redirect(url_for("login_Funcionario"))


@app.route("/inserir_Cardapio", methods=('POST', 'GET'))
def inserir_Cardapio():
    if 'funcionario_nome' in session:
        if request.method == "POST":
            cardapio = request.form.get("cardapio", "").strip()
            if cardapio:
                cardapioDB.inserir_Cardapio(cardapio)
                return redirect(url_for("cardapio"))
        return render_template("inserir_Cardapio.html")
    else: return redirect(url_for("login_Funcionario"))


@app.route("/cardapio")
def cardapio():
    cardapio = cardapioDB.ultimo_cardapio()
    return render_template("cardapio.html", cardapio=cardapio)

@app.route("/carnes", methods=("POST", "GET"))
def carnes():
    if 'funcionario_nome' in session:
        if request.method == "POST":
            try:
                carne = int(request.form.get("carne", "").strip())
            except (ValueError, AttributeError):
                carne = 0

            try:
                linguica = int(request.form.get("linguica", "").strip())
            except (ValueError, AttributeError):
                linguica = 0

            try:
                frango = int(request.form.get("frango", "").strip())
            except (ValueError, AttributeError):
                frango = 0
            carnesDB.modificar_Estoque(carne, linguica, frango)
        mantimentos = carnesDB.info_Estoque()
        mantimentos_carne = mantimentos['carne']
        mantimentos_linguica = mantimentos['linguica']
        mantimentos_frango = mantimentos['frango']
        data = mantimentos['data']
        return render_template("carnes.html", carne=mantimentos_carne, linguica=mantimentos_linguica, frango=mantimentos_frango, cardapio_Do_Dia=data)
    else: return redirect(url_for("login_Funcionario"))

@app.route("/novo_Dia")
def novo_Dia():
    if 'funcionario_nome' in session:
        carnesDB.inserir_Carnes(0, 0, 0)
        return redirect(url_for("carnes"))
    else: return redirect(url_for("login_Funcionario"))


@app.route("/historico_Dividas")
def historico_Dividas():
    if 'funcionario_nome' in session:
        dividas = dividasDB.listar_Dividas()
        return render_template("historico_Dividas.html" , dividas=dividas)
    else: 
        return redirect(url_for("login_Funcionario"))





@app.route("/adicionar_devedor", methods=("POST", "GET"))
def adicionar_devedor():
    if 'funcionario_nome' in session:
        if request.method == "POST":
            nome = request.form.get("devedor", "").strip()
            if nome:
                dividasDB.inserir_Devedor(nome)
        return render_template("adicionar_devedor.html")
    else: 
        return redirect(url_for("login_Funcionario"))    


@app.route("/lista_Devedores")
def lista_Devedores():
    if 'funcionario_nome' in session:
        devedores = dividasDB.listar_Devedores()
        return render_template("lista_Devedores.html", devedores=devedores)
    else: 
        return redirect(url_for("login_Funcionario"))  


@app.route("/devedores/<int:id>")
def devedor(id):
        if 'funcionario_nome' in session:
            dividas_Do_Devedor = dividasDB.pegar_Dividas(id)
            devedor = dividasDB.pegar_Devedor(id)
            if dividas_Do_Devedor :
                return render_template("devedor.html", dividas=dividas_Do_Devedor, id=id, devedor=devedor)
            else:
                return redirect(url_for("adicionar_divida", id=id))
            return render_template("devedor.html", dividas=dividas_Do_Devedor, id=id)
            
        else: 
            return redirect(url_for("login_Funcionario"))  


@app.route("/devedores/<int:id>/<int:id_divida>", methods = ("POST", "GET"))
def divida(id, id_divida):
    if 'funcionario_nome' in session:
        id = id
        devedor = dividasDB.pegar_Devedor(id)
        id_divida = id_divida
        divida = dividasDB.pegar_Divida(id_divida)
        return render_template("divida.html", divida=divida, devedor=devedor, id=id)
    else: 
        return redirect(url_for("login_Funcionario"))  


@app.route("/lista/<int:id_pedido>/entregue")
def pedidoEntregue(id_pedido):
    if 'funcionario_nome' in session:
        id = id_pedido
        pedidosDB.entregue(id)
        return redirect(url_for("lista"))  
    else:
        return redirect(url_for("login_Funcionario"))
    

@app.route("/lista/<int:id_pedido>/retirar")
def excluirPedido(id_pedido):
    if 'funcionario_nome' in session:
        id = id_pedido
        pedidosDB.retirar(id)
        return redirect(url_for("lista"))  
    else:
        return redirect(url_for("login_Funcionario"))
    

@app.route("/cliente_Perfil/<int:id>/<int:id_pedido>/cancelar")
def cancelarPedido(id, id_pedido):
    if 'nome_Cliente' in session:
        id = id
        id_pedido = id_pedido
        pedidosDB.canceladoCliente(id_pedido)
        return redirect(url_for("cliente_Perfil", id = id))
    else:
        return redirect(url_for("login_Funcionario"))


@app.route ("/cliente_Perfil/<int:id_cliente>/<int:id_pedido>/editar", methods=("POST", "GET"))
def editarPedido(id_cliente, id_pedido):
    if 'nome_Cliente' in session:
        mensagem = []
        if request.method == "POST":
            tipo_Feijao = request.form.get('tipo_Feijao', '')
            tipo_Arroz = request.form.get('tipo_Arroz', '')
            opcionais = request.form.getlist('opcionais')  
            carnes = request.form.getlist('carnes')        

            try:
                local_Entrega = request.form.get('local_Entrega', '').strip()
            except:
               mensagem.append = "Algo deu errado no local de entrega"
            if not local_Entrega:
                local_Entrega = 'Buscará no estabelecimento'
            preco = 12

            preco = 12 + 2 * sum(carne in carnes for carne in["Carne", "Frango", "Linguiça"])
            macarrao = "Sim" if "Macarrão" in opcionais else "Não"
            verduras = "Sim" if "Verduras" in opcionais else "Não"
            carne    = "Sim" if "Carne" in carnes else "Não"
            frango   = "Sim" if "Frango" in carnes else "Não"
            linguica = "Sim" if "Linguiça" in carnes else "Não"
            horario_Entrega = request.form.get('horario_Entrega', '').strip()
            obs = request.form.get('obs', '')
            pagamento = request.form.get("pagamento", "").strip()
            try:
                pedidosDB.editarPedido(tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica,
                    obs, horario_Entrega, local_Entrega, preco, pagamento, id_pedido)
            except:
                mensagem.append("Algo deu erradoao editar o pedido")
                return redirect(url_for("cliente_Perfil", id=id))
            id = id_cliente
        id_pedido = id_pedido
        pedido = pedidosDB.id_buscar(id_pedido)
        return render_template("editar_pedido.html",  pedido=pedido)
    else:
        return redirect(url_for("login_cliente"))
    

@app.route("/lista/historico")
def listaHistorico():
    if 'funcionario_nome' in session:
        pedidos = pedidosDB.listar_Pedidos_Historico()
        return render_template("lista_historico_quentinha.html", pedidos=pedidos)
    else:
        return redirect(url_for("login_Funcionario"))
    

@app.route("/cliente_Perfil/<int:id>/Historico")
def clienteHistorico(id):
    if 'nome_Cliente' in session:
        id = id
        pedidos = pedidosDB.pedidosDeClienteHistorico(id)
        return render_template("historico_Cliente.html", id=id, pedidos=pedidos)
    else:
        return redirect(url_for("login_cliente"))

@app.route("/devedores/<int:id>/adicionar_divida", methods=("POST", "GET"))
def adicionar_divida(id):
    if 'funcionario_nome' in session:
        id = id
        if request.method == "POST":
            valor = request.form.get("valor", "").strip()
            if "," in valor:
                valor_novo = valor.replace( "," , ".")
                valor = float(valor_novo)
            else:
                valor = float(valor)
            devedor = dividasDB.pegar_Devedor(id)
            nome = devedor["nome_Cliente"]
            dividasDB.inserir_Divida(id, nome, valor)
            return redirect(url_for("devedor", id=id))
        return render_template("adicionar_divida.html")
    else:
        return redirect(url_for("login_Funcionario"))



@app.route("/devedores/<int:id>/perdoar_divida/<int:id_Divida>")
def perdoar_divida(id, id_Divida):
    if 'funcionario_nome' in session:
        divida = dividasDB.pegar_Divida(id_Divida)
        valor = divida['valor']
        devedor = dividasDB.pegar_Devedor(id)
        total = devedor["total"]
        dividasDB.diminuir_divida(id, valor, total)
        dividasDB.excluir_Divida(id_Divida)
        return redirect(url_for("devedor", id=id))
    else:
        return redirect(url_for("login_Funcionario"))
if __name__ == "__main__":
    app.run(debug=True)