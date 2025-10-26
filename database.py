# Arquivo: database.py - Gerencia a leitura e escrita no arquivo data.json

import json
import os
import sys

# Adiciona o diretório atual ao PATH para garantir que os pacotes sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# Importa as classes dos pacotes para a reconstrução dos objetos
from core.cliente import Cliente
from core.produto import Produto
from core.pedido import Pedido


DB_FILE = 'data.json'

# --- DADOS INICIAIS (Em formato JSON PURO - Dicionários) ---
DADOS_INICIAIS = {
    'clientes': {
        '1': {'nome': "João Silva", 'cpf': "000.111.222-33", 'endereco': "Rua Principal"},
    }, 
    'produtos': {
        '101': {'nome': "PC Gamer Z100", 'preco': 6500.00}, 
        '102': {'nome': "Monitor Ultra", 'preco': 1200.00}
    }, 
    'pedidos': {}, 
    'next_ids': {'cliente': 2, 'pedido': 1}
}


def carregar_dados_json():
    """
    Objetivo: Carregar dados do arquivo JSON e reconstruir os objetos Python.
    Função: Lida com a leitura do disco e chama o método estático 'from_json' 
            de cada classe para recriar as instâncias.
    """
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump(DADOS_INICIAIS, f, indent=4)
        data = DADOS_INICIAIS
    else:
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("AVISO: Arquivo data.json corrompido. Iniciando com dados padrão.")
            data = DADOS_INICIAIS

    # Reconstrução dos Objetos (De JSON para Instâncias Python)
    produtos_obj = {pid: Produto.from_json(d) for pid, d in data['produtos'].items()}
    clientes_obj = {cid: Cliente.from_json(d) for cid, d in data['clientes'].items()}
    
    pedidos_obj = {}
    for pid, d in data['pedidos'].items():
        try:
            cliente_ref = clientes_obj.get(d['cliente_id']) 
            if cliente_ref:
                # O from_json do Pedido lida com a Composição (itens)
                pedido_obj = Pedido.from_json(d, cliente_ref, produtos_obj)
                pedidos_obj[pid] = pedido_obj
        except Exception as e:
            print(f"Erro ao reconstruir Pedido {pid}: {e}. Ignorando.")

    return {
        'clientes': clientes_obj,
        'produtos': produtos_obj,
        'pedidos': pedidos_obj,
        'next_ids': data.get('next_ids', {'cliente': 1, 'pedido': 1})
    }

def salvar_dados_json(dados):
    """
    Objetivo: Serializar os objetos Python para JSON e salvar no arquivo.
    Função: Chama o método 'to_json()' de cada objeto e salva o resultado.
    """
    data_to_save = {
        'clientes': {cid: obj.to_json() for cid, obj in dados['clientes'].items()},
        'produtos': {pid: obj.to_json() for pid, obj in dados['produtos'].items()},
        'pedidos': {pid: obj.to_json() for pid, obj in dados['pedidos'].items()},
        'next_ids': dados['next_ids']
    }
    
    with open(DB_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=4)