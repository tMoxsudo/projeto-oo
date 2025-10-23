# Arquivo: pagamentos/pagamento_cartao.py
from .pagamento import Pagamento # IMPORTAÇÃO RELATIVA CORRETA

class PagamentoCartao(Pagamento):
    """
    Subclasse Concreta.
    Objetivo: Implementar a lógica de pagamento via cartão (POLIMORFISMO - Implementação 1).
    """
    def __init__(self, valor=0.0, num_cartao=""):
        super().__init__(valor)
        self.num_cartao = num_cartao
    
    def processar(self):
        """Implementação Polimórfica 1."""
        print(f"   Processando R$ {self.valor:.2f} via Cartão (Final {self.num_cartao[-4:]}).")
        print("   -> **TESTE POLIMORFISMO**: Lógica de Cartão aplicada (Taxa de 5%).")