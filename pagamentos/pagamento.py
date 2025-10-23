# Arquivo: pagamentos/pagamento.py
from abc import ABC, abstractmethod

class Pagamento(ABC):
    """
    Classe Abstrata (Interface).
    Objetivo: Definir o contrato do método 'processar()'. Base do POLIMORFISMO e alvo da DEPENDÊNCIA.
    """
    def __init__(self, valor=0.0):
        self.valor = valor

    @abstractmethod
    def processar(self):
        """Método abstrato. Deve ser implementado pelas subclasses."""
        pass
    
    def to_json(self):
        """Serializa o valor do pagamento."""
        return {'valor': self.valor, 'tipo': self.__class__.__name__}