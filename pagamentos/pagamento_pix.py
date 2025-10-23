# Arquivo: pagamentos/pagamento_pix.py
from .pagamento import Pagamento # IMPORTAÇÃO RELATIVA CORRETA

class PagamentoPix(Pagamento):
    """
    Subclasse Concreta.
    Objetivo: Implementar a lógica de pagamento via Pix (POLIMORFISMO - Implementação 2).
    """
    def __init__(self, valor=0.0, chave_pix=""):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
        """Implementação Polimórfica 2."""
        print(f"   Processando R$ {self.valor:.2f} via Pix (Chave: {self.chave_pix}).")
        print("   -> **TESTE POLIMORFISMO**: Lógica de Pix aplicada (Confirmação imediata).")