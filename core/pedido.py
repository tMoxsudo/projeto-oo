# Arquivo: core/pedido.py
from .cliente import Cliente
from .item_pedido import ItemPedido
from .produto import Produto 
from pagamentos.pagamento import Pagamento # IMPORTAÇÃO EXTERNA

class Pedido:
    """
    Classe de Transação.
    Objetivo: Orquestrar ASSOCIAÇÃO (Cliente), COMPOSIÇÃO (ItemPedido) e 
              DEPENDÊNCIA/POLIMORFISMO (Pagamento).
    """
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens = [] 
        self.pago = False

    def adicionar_item(self, produto: Produto, quantidade: int):
        """Função de Composição: anexa ItemPedido ao Pedido."""
        item = ItemPedido(produto, quantidade)
        self.itens.append(item)

    def calcular_total(self):
        return sum(item.subtotal for item in self.itens)

    def finalizar_compra(self, forma_pagamento: Pagamento):
        """
        Função de Dependência e Polimorfismo.
        Objetivo: Usa 'forma_pagamento' (DEPENDÊNCIA) e chama seu método 'processar()' 
                  (POLIMORFISMO).
        """
        total = self.calcular_total()
        
        print("\n" + "="*70)
        print(f"** PROCESSANDO PAGAMENTO - Cliente: {self.cliente.nome} | Total: R$ {total:.2f} **")
        
        forma_pagamento.valor = total
        forma_pagamento.processar() # Chamada polimórfica
        print("="*70)
        self.pago = True

    def to_json(self):
        """Serializa o Pedido, salvando apenas o ID do cliente (Associação)."""
        # (Lógica para obter o ID do cliente - simplificada)
        cliente_id = [cid for cid, c in Cliente.db_ref.items() if c is self.cliente][0] if hasattr(Cliente, 'db_ref') else None
        
        return {
            'cliente_id': cliente_id,
            'itens': [item.to_json() for item in self.itens], # Composição
            'pago': self.pago
        }

    @staticmethod
    def from_json(data, cliente_ref: Cliente, produtos_db):
        """Reconstrói o Pedido, restaurando a Associação e Composição."""
        pedido = Pedido(cliente_ref)
        pedido.pago = data.get('pago', False)
        
        # Reconstroi os itens (Composição)
        for item_data in data['itens']:
            item = ItemPedido.from_json(item_data)
            pedido.itens.append(item)
            
        return pedido