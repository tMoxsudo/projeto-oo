# Arquivo: app_web.py - Servidor Flask para a Interface Web

from flask import Flask, render_template, request, redirect, url_for
import database # Importa o módulo de persistência
from core.cliente import Cliente # Importa o modelo Cliente

# 1. Configuração Inicial
app = Flask(__name__)
DB = database.carregar_dados_json() # Carrega todos os objetos do JSON na memória


@app.route('/')
def index():
    """
    Rota principal. Exibe a lista de todos os modelos (Clientes e Produtos).
    """
    clientes_data = DB['clientes'].items()
    produtos_data = DB['produtos'].items()
    
    return render_template(
        'index.html',
        clientes=clientes_data,
        produtos=produtos_data
    )


@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente_web():
    """
    Rota para cadastrar um novo Cliente.
    GET: Exibe o formulário.
    POST: Processa o envio do formulário, cria o objeto Cliente (TESTE HERANÇA).
    """
    if request.method == 'POST':
        # 1. Captura dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        
        # 2. Instanciação e Herança (Lógica POO)
        novo_cliente = Cliente(nome, cpf, endereco)
        
        # 3. Persistência
        cliente_id = str(DB['next_ids']['cliente'])
        DB['clientes'][cliente_id] = novo_cliente
        DB['next_ids']['cliente'] += 1
        database.salvar_dados_json(DB)
        
        # Redireciona de volta para a lista principal
        return redirect(url_for('index'))
    
    # Se for GET, simplesmente renderiza o formulário de cadastro
    return render_template('cadastro.html')


if __name__ == '__main__':
    print("\n* Servidor Flask rodando em: http://127.0.0.1:5000/")
    # ATENÇÃO: Execute este arquivo a partir da raiz do projeto usando 'python3 app_web.py'
    app.run(debug=True)