# Arquivo: core/cliente.py
from .pessoa import Pessoa # IMPORTAÇÃO RELATIVA CORRETA

class Cliente(Pessoa):
    """
    Classe Concreta.
    Objetivo: Demonstrar HERANÇA (extensão de Pessoa), POLIMORFISMO (apresentar_dados)
              e participa da ASSOCIAÇÃO (com Pedido).
    """
    def __init__(self, nome, cpf, endereco):
        super().__init__(nome, cpf) # Chamada ao construtor da superclasse (Herança)
        self.endereco = endereco

    def apresentar_dados(self):
        """Método Sobrescrito para demonstrar o POLIMORFISMO."""
        dados_base = super().apresentar_dados()
        return f"{dados_base}, Endereço: {self.endereco} (CLIENTE)"
    
    def to_json(self):
        """Serializa o Cliente, incluindo atributos herdados."""
        base_data = super().to_json()
        base_data['endereco'] = self.endereco
        return base_data

    @staticmethod
    def from_json(data):
        """Reconstrói a instância de Cliente a partir dos dados JSON."""
        return Cliente(data['nome'], data['cpf'], data['endereco'])