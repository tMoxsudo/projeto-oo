# Arquivo: core/item_pedido.py
from .produto import Produto # IMPORTAÇÃO RELATIVA CORRETA

class ItemPedido:
    """
    Classe Parte (na Composição).
    Objetivo: Representar uma linha de produto. Sua existência depende da classe 'Pedido'.
    """
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
        self.subtotal = produto.preco * quantidade

    def to_json(self):
        """Serializa o ItemPedido para salvar como parte do Pedido."""
        return {
            'produto_data': self.produto.to_json(),
            'quantidade': self.quantidade
        }
    
    @staticmethod
    def from_json(data):
        """Reconstrói a instância de ItemPedido (usado na desserialização de Pedido)."""
        produto_obj = Produto.from_json(data['produto_data'])
        return ItemPedido(produto_obj, data['quantidade'])

    def __str__(self):
        return f"   - {self.quantidade}x {self.produto.nome} (R$ {self.subtotal:.2f})"