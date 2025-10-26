# Arquivo: app_web.py - Servidor Flask (Controlador Web)

from flask import Flask, render_template, request, redirect, url_for
import database # Importa o módulo de persistência (database.py)

# Importa os modelos de domínio
from core.cliente import Cliente
from core.produto import Produto
from core.pedido import Pedido 
from pagamentos.pagamento_cartao import PagamentoCartao
from pagamentos.pagamento_pix import PagamentoPix


# 1. Configuração Inicial do Flask
app = Flask(__name__, template_folder='templates') 

# Carrega o estado do sistema do JSON para a memória no início
DB = database.carregar_dados_json() 

# Associa a referência do dicionário de clientes ao objeto Cliente (necessário para serialização do Pedido)
Cliente.db_ref = DB['clientes'] 


# ----------------------------------------------------------------------
# ROTAS DE VISUALIZAÇÃO E LISTAGEM
# ----------------------------------------------------------------------

@app.route('/')
def index():
    """
    Endpoint: index (Rota: /)
    Objetivo: Rota principal. Carrega o estado atual dos modelos e renderiza o Dashboard.
    """
    clientes_data = DB['clientes'].items()
    produtos_data = DB['produtos'].items()
    pedidos_data = DB['pedidos'].items()

    # Renderiza o template principal (Dashboard)
    return render_template(
        'dashboard.html', # CHAMA O ARQUIVO CORRETO
        clientes=clientes_data,
        produtos=produtos_data,
        pedidos=pedidos_data
    )


# ----------------------------------------------------------------------
# ROTAS DE CRIAÇÃO E LÓGICA DE NEGÓCIO
# ----------------------------------------------------------------------

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente_web():
    """
    Endpoint: cadastrar_cliente_web (Rota: /cadastrar_cliente)
    Demonstra: HERANÇA.
    """
    if request.method == 'POST':
        # 1. Captura e Instanciação
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        
        # Lógica POO (Herança)
        novo_cliente = Cliente(nome, cpf, endereco)
        
        # 2. Persistência
        cliente_id = str(DB['next_ids']['cliente'])
        DB['clientes'][cliente_id] = novo_cliente
        DB['next_ids']['cliente'] += 1
        database.salvar_dados_json(DB)
        
        return redirect(url_for('index'))
    
    # GET: Exibe o formulário
    return render_template('cadastro_cliente.html')


@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido_web():
    """
    Endpoint: cadastrar_pedido_web (Rota: /cadastrar_pedido)
    Demonstra: ASSOCIAÇÃO e COMPOSIÇÃO.
    """
    clientes_data = DB['clientes']
    produtos_data = DB['produtos']

    if request.method == 'POST':
        # 1. Captura e validação
        cliente_id = request.form.get('cliente_id')
        produtos_ids = request.form.getlist('produto_id')
        
        cliente_obj = clientes_data.get(cliente_id)

        if not cliente_obj:
            return render_template('error.html', message="Cliente não encontrado."), 400

        novo_pedido = Pedido(cliente_obj) # ASSOCIAÇÃO

        # 2. Processamento dos Itens (Composição)
        total_itens_adicionados = 0
        for produto_id in produtos_ids:
            qtde_campo = f'quantidade_{produto_id}'
            try:
                quantidade = int(request.form.get(qtde_campo, 0))
            except ValueError:
                quantidade = 0
            
            produto_obj = produtos_data.get(produto_id)
            
            if produto_obj and quantidade > 0:
                novo_pedido.adicionar_item(produto_obj, quantidade) # COMPOSIÇÃO
                total_itens_adicionados += 1

        if total_itens_adicionados == 0:
            return render_template('error.html', message="O pedido deve ter pelo menos um item."), 400

        # 3. Persistência
        pedido_id = str(DB['next_ids']['pedido'])
        DB['pedidos'][pedido_id] = novo_pedido
        DB['next_ids']['pedido'] += 1
        database.salvar_dados_json(DB)
        
        return redirect(url_for('index'))

    # GET: Exibe o formulário
    return render_template(
        'cadastro_pedido.html', 
        clientes=clientes_data.items(), 
        produtos=produtos_data.items()
    )


if __name__ == '__main__':
    # Para rodar, o terminal deve estar na raiz do PROJETO OO
    # Execute: python3 app_web.py
    app.run(debug=True)