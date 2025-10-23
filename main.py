# Arquivo: main.py - Menu Interativo com Persistência JSON

# ---------------------------------------------------------------------
# IMPORTAÇÕES E INICIALIZAÇÃO
# ---------------------------------------------------------------------

# Importações dos pacotes de classes (Necessárias para instanciar objetos)
from core.cliente import Cliente
from core.produto import Produto
from core.pedido import Pedido
from pagamentos.pagamento_cartao import PagamentoCartao
from pagamentos.pagamento_pix import PagamentoPix

# Importação do módulo de persistência (no mesmo nível)
import database


# Carrega o estado do sistema do JSON para a memória
try:
    DB = database.carregar_dados_json()
    clientes_db = DB['clientes']
    produtos_db = DB['produtos']
    pedidos_db = DB['pedidos']
    next_ids = DB['next_ids']

    # REFÊNCIA GLOBAL para a serialização correta do Pedido (Associação)
    # Objetivo: Permite que o Pedido encontre o ID do Cliente ao salvar no JSON.
    Cliente.db_ref = clientes_db 

except Exception as e:
    print(f"\nERRO CRÍTICO NA INICIALIZAÇÃO: Não foi possível carregar o banco de dados. {e}")
    # Encerra o programa se o DB falhar para evitar corrupção
    exit(1)


def salvar_e_sair():
    """
    Função: Encerra o loop principal do programa.
    Objetivo: Chamar o método de persistência final para garantir que o estado
              do sistema seja salvo no data.json antes de sair.
    """
    database.salvar_dados_json(DB)
    print("Dados salvos. Saindo do sistema. Até logo!")


# ---------------------------------------------------------------------
# FUNÇÕES DE LÓGICA E POO
# ---------------------------------------------------------------------

def cadastrar_cliente_func():
    """
    Funcionalidade: Cadastro de um novo Cliente (Opção 1).
    Objetivo: Demonstrar a HERANÇA (instanciando Cliente) e o POLIMORFISMO 
              (chamando o método sobrescrito apresentar_dados).
    """
    global next_ids
    print("\n--- 1. CADASTRO DE CLIENTE (TESTE HERANÇA) ---")
    
    nome = input("Nome: ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    
    # Herança: Cria um objeto Cliente
    novo_cliente = Cliente(nome, cpf, endereco)
    
    # Persistência
    cliente_id = str(next_ids['cliente'])
    clientes_db[cliente_id] = novo_cliente
    next_ids['cliente'] += 1
    database.salvar_dados_json(DB)
    
    # Teste de Output (Polimorfismo por Sobrescrita)
    print(f"\n[SUCESSO] Cliente ID {cliente_id} cadastrado.")
    print(f"Dados (Polimórficos): {novo_cliente.apresentar_dados()}")


def listar_entidades_func():
    """
    Funcionalidade: Listagem de Modelos (Opção 2).
    Objetivo: Exibir todos os objetos persistidos (Clientes, Produtos, Pedidos),
              confirmando que a desserialização (from_json) funcionou.
    """
    print("\n--- 2. LISTAGEM DE MODELOS ---")
    
    if not clientes_db and not produtos_db and not pedidos_db:
        print("[AVISO] Nenhuma entidade cadastrada para exibição.")
        return

    print(f"\n[CLIENTES] Total: {len(clientes_db)}")
    for cid, cliente in clientes_db.items():
        print(f"ID {cid}: {cliente.nome} ({cliente.cpf})")

    print(f"\n[PRODUTOS] Total: {len(produtos_db)}")
    for pid, produto in produtos_db.items():
        print(f"ID {pid}: {produto.nome} (R$ {produto.preco:.2f})")
    
    print(f"\n[PEDIDOS] Total: {len(pedidos_db)}")
    for pid, pedido in pedidos_db.items():
        status = 'PAGO' if pedido.pago else 'ABERTO'
        print(f"Pedido ID {pid}: Cliente {pedido.cliente.nome}, Total R$ {pedido.calcular_total():.2f} (Status: {status})")


def criar_pedido_func():
    """
    Funcionalidade: Criação de Pedido (Opção 3).
    Objetivo: Demonstrar ASSOCIAÇÃO (Cliente-Pedido) e COMPOSIÇÃO (Pedido-ItemPedido).
    """
    global next_ids
    print("\n--- 3. CRIAR NOVO PEDIDO (TESTE COMPOSIÇÃO/ASSOCIAÇÃO) ---")
    
    # 1. Seleção do Cliente (Teste Associação)
    listar_entidades_func()
    
    if not clientes_db:
        print("[ERRO] Não há clientes cadastrados. Crie um cliente primeiro.")
        return
        
    cliente_id = input("\nDigite o ID do Cliente para o pedido: ")
    cliente_obj = clientes_db.get(cliente_id)
    if not cliente_obj:
        print("[ERRO] Cliente não encontrado. Retornando ao menu.")
        return 
        
    # Associação: Cria o Pedido com a referência ao Cliente
    novo_pedido = Pedido(cliente_obj)
    
    # 2. Adicionar Itens (Teste Composição)
    print("\n--- ADICIONAR ITENS (Teste Composição) ---")
    while True:
        pid = input("ID do Produto (ou 'f' para finalizar): ")
        if pid == 'f':
            break
        
        produto_obj = produtos_db.get(pid)
        if produto_obj:
            try:
                qtde = int(input("Quantidade: "))
                if qtde > 0:
                    # Composição: ItemPedido é criado e contido no Pedido
                    novo_pedido.adicionar_item(produto_obj, qtde) 
                    print(f"Item adicionado. Subtotal atual: R$ {novo_pedido.calcular_total():.2f}")
                else:
                    print("[AVISO] Quantidade deve ser positiva.")
            except ValueError:
                print("[ERRO] Quantidade inválida.")
        else:
            print("[ERRO] Produto não encontrado.")
            
    if novo_pedido.calcular_total() == 0:
        print("[AVISO] Pedido vazio. Cancelando e voltando ao menu.")
        return
        
    # 3. Persistência
    pedido_id = str(next_ids['pedido'])
    pedidos_db[pedido_id] = novo_pedido
    next_ids['pedido'] += 1
    
    print(f"\n[SUCESSO] Pedido ID {pedido_id} criado e salvo. Total: R$ {novo_pedido.calcular_total():.2f}")
    database.salvar_dados_json(DB)


def processar_pagamento_func():
    """
    Funcionalidade: Processar Pagamento (Opção 4).
    Objetivo: Demonstrar DEPENDÊNCIA (Pedido usa Pagamento) e POLIMORFISMO 
              (diferentes execuções do método processar()).
    """
    print("\n--- 4. PROCESSAR PAGAMENTO (TESTE POLIMORFISMO/DEPENDÊNCIA) ---")
    
    # 1. Selecionar Pedido
    listar_entidades_func()
    pid = input("\nDigite o ID do Pedido para pagar: ")
    pedido_obj = pedidos_db.get(pid)
    
    if not pedido_obj:
        print("[ERRO] Pedido não encontrado. Retornando ao menu.")
        return
    if pedido_obj.pago:
        print("[AVISO] Pedido já foi pago. Retornando ao menu.")
        return
    
    total = pedido_obj.calcular_total()
    
    # 2. Selecionar Forma de Pagamento (Teste Polimorfismo)
    print(f"Total a pagar: R$ {total:.2f}")
    print("Selecione a forma de pagamento:")
    print("1: Cartão de Crédito (Teste Polimorfismo 1)")
    print("2: Pix (Teste Polimorfismo 2)")
    escolha = input("Opção: ")
    
    forma_pagamento = None
    if escolha == '1':
        # Polimorfismo: Cria a subclasse PagamentoCartao
        forma_pagamento = PagamentoCartao(valor=total, num_cartao="**** **** **** 3456")
    elif escolha == '2':
        # Polimorfismo: Cria a subclasse PagamentoPix
        forma_pagamento = PagamentoPix(valor=total, chave_pix="mariapix@email.com")
    else:
        print("[ERRO] Opção inválida. Retornando ao menu.")
        return

    # 3. Execução da Lógica POO
    # Dependência: O Pedido utiliza o objeto Pagamento
    # Polimorfismo: O método processar() correto é chamado
    pedido_obj.finalizar_compra(forma_pagamento)

    # 4. Finalização e Persistência
    pedido_obj.pago = True
    database.salvar_dados_json(DB) 
    print(f"\n[SUCESSO] Pagamento do Pedido {pid} processado e salvo. Status: PAGO.")


def exibir_menu():
    """
    Função: Exibir as opções disponíveis para o usuário no terminal.
    Objetivo: Ser a interface de entrada de dados do sistema.
    """
    print("\n" + "="*50)
    print("    SISTEMA DE LOJA ONLINE (JSON PERSISTÊNCIA)    ")
    print("="*50)
    print("1: Cadastrar Cliente (Teste Herança)")
    print("2: Listar Entidades (Visualizar Modelos)")
    print("3: Criar Novo Pedido (Teste Composição/Associação)")
    print("4: Processar Pagamento (Teste Polimorfismo/Dependência)")
    print("0: Sair e Salvar Dados")
    print("="*50)

# ---------------------------------------------------------------------
# LOOP PRINCIPAL DO PROGRAMA (GARANTE ESTABILIDADE)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        try:
            exibir_menu()
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                cadastrar_cliente_func()
            elif opcao == '2':
                listar_entidades_func()
            elif opcao == '3':
                criar_pedido_func()
            elif opcao == '4':
                processar_pagamento_func()
            elif opcao == '0':
                salvar_e_sair()
                break
            else:
                print("Opção inválida. Tente novamente.")
                
        except Exception as e:
            # Captura qualquer erro inesperado e volta ao menu
            print(f"\n[ERRO INESPERADO] Ocorreu um erro: {e}. Voltando ao menu principal.")
            # Este bloco garante que o loop while True não seja quebrado acidentalmente.