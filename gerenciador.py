"""
Módulo de Gerenciamento (Back-end)
Responsável por gerenciar as despesas, incluindo a adição e listagem de despesas.
"""
# Funções de gerenciamento de despesas

def adicionar_despesa(lista_despesas, nova_despesa):
    """
    Adiciona uma nova despesa formatada à lista principal.
    """

    lista_despesas.append(nova_despesa)

def listar_despesas(lista_despesas):
    """
    Exibe todas as despesas cadastradas na lista principal.
    Além de verificar se a lista está vazia, caso esteja, 
    retorna uma mensagem informando que não há despesas cadastradas.
    """
    if not lista_despesas:
        print("\n" + "Nenhuma despesa cadastrada!")
    else:
        for indice, despesa in enumerate(lista_despesas, start=1):
            print(f"{indice} - {despesa}")