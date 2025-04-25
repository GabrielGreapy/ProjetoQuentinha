from flask import *



app = Flask(__name__)
import pedidosDB
import administracaoDB
import cardapioDB
import carnesDB
import dividasDB
app.config['SECRET_KEY'] = 'bananadog'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pedindo", methods=('POST', 'GET'))
def pedindo():
    mensagem = 'Pode fazer seu pedido'
    
    if request.method == 'POST':
        nome_Cliente = session['nome_Cliente']
        id_Cliente = session['id_Cliente']
        if nome_Cliente != '':
            tipo_Feijao = request.form.get('tipo_Feijao', '')
            tipo_Arroz = request.form.get('tipo_Arroz', '')
            
            
            opcionais = request.form.getlist('opcionais')  
            carnes = request.form.getlist('carnes')        

            local_Entrega = request.form.get('local_Entrega', '').strip()
            
            if not local_Entrega:
                local_Entrega = 'Buscará no estabelecimento'
            preco = 12
            macarrao = "Não"
            verduras = "Não"
            frango = "Não"
            carne = "Não"
            linguica = "Não"

            
            if "macarrao" in opcionais:
                macarrao = "Sim"
                
            if "verduras" in opcionais:
                verduras = "Sim"

            if "carne" in carnes:
                carne = "Sim"
                preco += 2
            if "frango" in carnes:
                frango = "Sim"
                preco += 2
            if "linguica" in carnes:
                linguica = "Sim"
                preco += 2
            horario_Entrega = request.form.get('horario_Entrega', '').strip()
            obs = request.form.get('obs', '')
            pagamento = request.form.get("pagamento", "").strip()
            pedidosDB.inserir(id_Cliente, nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica, obs, preco, horario_Entrega, local_Entrega, pagamento)
            mensagem = 'Pedido mandado, muito bem'
            return redirect(url_for("cliente_Perfil", id=session['id_Cliente']))
        else:
            mensagem = 'O seu nome está em branco, por favor informe-nos um nome para que possamos distinguir seu pedido'

    return render_template("pedindo_Quentinha.html", mensagem=mensagem)


@app.route("/lista")
def lista():
    if 'funcionario_nome' in session:
        pedidos= pedidosDB.listar_Pedidos()
        mensagem="Esta é a lista de pedidos"
        return render_template("lista_pedidos.html", mensagem=mensagem, pedidos=pedidos)



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
    mensagem= ''
    if request.method == 'POST':
        nome = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        if nome and senha:
            funcionario = administracaoDB.pegar_Funcionarios(nome, senha)
            if funcionario:
                session['funcionario_id'] = funcionario['id_funcionario']
                session['funcionario_nome'] = funcionario['nome_Funcionario']
                return redirect(url_for('funcionario'))
            else: mensagem='Funcionário não existe.' 
        else: mensagem= 'Escreva algo nos campos'
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
    mensagem = ''
    if request.method == "POST":
        nome = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        if nome and senha:
            
            cliente = administracaoDB.pegar_Clientes(nome, senha)
            if cliente:
                session['nome_Cliente'] = cliente['nome_Cliente']
                session['numero_Cliente'] = cliente['numero_Cliente']
                session['id_Cliente'] = cliente['id_Cliente']
                return redirect(url_for("cliente_Perfil", id=session['id_Cliente']))
            else: mensagem = 'Cliente não existe'
        else: mensagem = 'Preencha as informações'
    return render_template("login_cliente.html", mensagem=mensagem)


@app.route("/cliente_Perfil/<int:id>")
def cliente_Perfil(id):
    if 'nome_Cliente' in session:
        id = id
        nome = session['nome_Cliente']
        numero = session['numero_Cliente']
        pedidos = pedidosDB.pedidosDeCliente(id)
        return render_template("cliente_Perfil.html", nome=nome , numero=numero, pedidos=pedidos)
    else: return redirect(url_for("/login_cliente"))


@app.route("/criar_Cliente", methods=( "POST", "GET"))
def criar_Cliente():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        nome = request.form.get("nome", "").strip()
        numero = request.form.get("numero", "").strip()
        senha = request.form.get("senha", "").strip()
        administracaoDB.inserir_Cliente( email, nome, numero, senha)
        return redirect(url_for("login_cliente"))    
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
            
            carne = int(request.form.get("carne", 0))
            linguica = int(request.form.get("linguica", 0))
            frango = int(request.form.get("frango", 0))
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





@app.route("/adicionar_Conta", methods=("POST", "GET"))
def adicionar_Conta():
    if 'funcionario_nome' in session:
        if request.method == "POST":
            nome = request.form.get("devedor", "").strip()
            if nome:
                dividasDB.inserir_Devedor(nome)
        return render_template("adicionar_Conta.html")
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
            total = 0
            for divida in dividas_Do_Devedor:
                conta = divida[3]
                if "," in conta:
                    conta_nova = conta.replace( "," , ".")
                    conta = float(conta_nova)
                total += conta
            return render_template("devedor.html", dividas=dividas_Do_Devedor, id=id, total=total)
        else: 
            return redirect(url_for("login_Funcionario"))  


@app.route("/devedores/<int:id>/<int:id_divida>", methods = ("POST", "GET"))
def divida(id, id_divida):
    if 'funcionario_nome' in session:
        id = id
        devedor = dividasDB.pegar_Devedor(id)
        id_divida = id_divida
        divida = dividasDB.pegar_Divida(id_divida)

        return render_template("divida.html", divida=divida, devedor=devedor)
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
        if request.form == "POST":
            id = id_cliente
            id_pedido = id_pedido
            return redirect(url_for("cliente_Perfil", id = id))
        return render_template("editar_pedido.html")
    else:
        return redirect(url_for("/login_cliente"))

if __name__ == "__main__":
    app.run(debug=True)