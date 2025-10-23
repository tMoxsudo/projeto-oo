# Arquivo: core/pessoa.py

class Pessoa:
    """
    Classe Abstrata Base.
    Objetivo: Definir atributos comuns (nome, cpf) para demonstrar a HERANÇA.
    """
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def apresentar_dados(self):
        """Método base para ser sobrescrito (Polimorfismo)."""
        return f"Nome: {self.nome}, CPF: {self.cpf}"
    
    def to_json(self):
        """Serializa os atributos da Pessoa para JSON."""
        return {'nome': self.nome, 'cpf': self.cpf}