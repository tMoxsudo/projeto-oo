# Arquivo: core/produto.py

class Produto:
    """
    Classe de Domínio.
    Objetivo: Representar o item vendido, usado pela classe ItemPedido.
    """
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def to_json(self):
        """Serializa o Produto."""
        return {'nome': self.nome, 'preco': self.preco}
    
    @staticmethod
    def from_json(data):
        """Reconstrói a instância de Produto a partir dos dados JSON."""
        return Produto(data['nome'], data['preco'])