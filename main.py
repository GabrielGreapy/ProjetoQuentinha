from flask import *



app = Flask(__name__)
import pedidosDB
app.config['SECRET_KEY'] = 'bananadog'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pedindo", methods=('POST', 'GET'))
def pedindo():
    mensagem = 'Pode fazer seu pedido'
    
    if request.method == 'POST':
        nome_Cliente = request.form.get('nome_Cliente', '').strip()
        
        if nome_Cliente != '':
            tipo_Feijao = request.form.get('tipo_Feijao', '')
            tipo_Arroz = request.form.get('tipo_Arroz', '')
            
            
            opcionais = request.form.getlist('opcionais')  
            carnes = request.form.getlist('carnes')        

            preco = 12
            macarrao = "nao"
            verduras = "nao"
            frango = "nao"
            carne = "nao"
            linguica = "nao"

            
            if "macarrao" in opcionais:
                macarrao = "sim"
                
            if "verduras" in opcionais:
                verduras = "sim"

            if "carne" in carnes:
                carne = "sim"
                preco += 2
            if "frango" in carnes:
                frango = "sim"
                preco += 2
            if "linguica" in carnes:
                linguica = "sim"
                preco += 2

            obs = request.form.get('obs', '')

            pedidosDB.inserir(nome_Cliente, tipo_Feijao, tipo_Arroz, macarrao, verduras, frango, carne, linguica, obs, preco)
            mensagem = 'Pedido mandado, muito bem'
            return redirect("lista")
        else:
            mensagem = 'O seu nome está em branco, por favor informe-nos um nome para que possamos distinguir seu pedido'

    return render_template("pedindo_Quentinha.html", mensagem=mensagem)


@app.route("/lista")
def lista():
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




















if __name__ == "__main__":
    app.run(debug=True)