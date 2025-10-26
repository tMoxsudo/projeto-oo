# Arquivo: app_web.py - Servidor Flask para a Interface Web

from flask import Flask, render_template, request, redirect, url_for
import database 
from core.cliente import Cliente
from core.produto import Produto
from core.pedido import Pedido 

# 1. Configuração Inicial
app = Flask(__name__, template_folder='templates') # Define o local dos templates
DB = database.carregar_dados_json()


@app.route('/')
def index():
    """
    Rota principal. Exibe a lista de todos os modelos persistidos.
    """
    clientes_data = DB['clientes'].items()
    produtos_data = DB['produtos'].items()
    pedidos_data = DB['pedidos'].items()

    return render_template(
        'index.html',
        clientes=clientes_data,
        produtos=produtos_data,
        pedidos=pedidos_data
    )


@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente_web():
    """
    Rota para cadastrar um novo Cliente (Teste HERANÇA).
    """
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        
        # Instanciação e Herança (Lógica POO)
        novo_cliente = Cliente(nome, cpf, endereco)
        
        # Persistência
        cliente_id = str(DB['next_ids']['cliente'])
        DB['clientes'][cliente_id] = novo_cliente
        DB['next_ids']['cliente'] += 1
        database.salvar_dados_json(DB)
        
        return redirect(url_for('index'))
    
    return render_template('cadastro_cliente.html')


@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido_web():
    """
    Rota para cadastrar um novo Pedido. 
    Demonstra a Associação (Cliente) e Composição (ItemPedido).
    """
    clientes_data = DB['clientes']
    produtos_data = DB['produtos']

    if request.method == 'POST':
        # 1. Captura e validação
        cliente_id = request.form.get('cliente_id')
        produtos_ids = request.form.getlist('produto_id') 
        
        cliente_obj = clientes_data.get(cliente_id)

        if not cliente_obj:
            return "Erro: Cliente não encontrado.", 400

        novo_pedido = Pedido(cliente_obj) # ASSOCIAÇÃO: Referência ao objeto Cliente

        # 2. Adicionar Itens (Composição)
        total_itens = 0
        for produto_id in produtos_ids:
            # Pega a quantidade correta para o produto_id específico
            qtde_campo = f'quantidade_{produto_id}'
            try:
                quantidade = int(request.form.get(qtde_campo, 0))
            except ValueError:
                quantidade = 0
            
            produto_obj = produtos_data.get(produto_id)
            
            if produto_obj and quantidade > 0:
                # COMPOSIÇÃO: ItemPedido criado e anexado ao Pedido
                novo_pedido.adicionar_item(produto_obj, quantidade)
                total_itens += 1

        if total_itens == 0:
            return "Erro: O pedido deve ter pelo menos um item.", 400

        # 3. Persistência
        pedido_id = str(DB['next_ids']['pedido'])
        DB['pedidos'][pedido_id] = novo_pedido
        DB['next_ids']['pedido'] += 1
        database.salvar_dados_json(DB)
        
        return redirect(url_for('index'))

    # Se for GET, exibe o formulário
    return render_template(
        'cadastro_pedido.html', 
        clientes=clientes_data.items(), 
        produtos=produtos_data.items()
    )


if __name__ == '__main__':
    # Para rodar, o terminal deve estar na raiz do PROJETO OO
    app.run(debug=True)