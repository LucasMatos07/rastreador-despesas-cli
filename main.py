"""
Módulo Principal (Front-end / CLI)
Responsável pela interface de usuário via terminal, exibição do menu
e controle de fluxo de execução do programa.
"""

# Importação das funções

from gerenciador import adicionar_despesa, listar_despesas

# Declaração das váriasveis

despesas = []

# Listagem das funções
    
while True:
    print ("\n" + "="*30)
    print ("\n" + "Oque iremos realizar hoje?")
    print ("\n" + "="*30)
    print ("\n" + "1 - Adicionar despesa")
    print ("2 - Listar despesas")
    print ("3 - Sair do programa")

    opcao = input("\n" + "Selecione uma opção: ")

    if opcao == "1":
        nome_despesa =input("\n" + "Digite o nome da despesa: ").title().strip()

        adicionar_despesa(despesas, nome_despesa)

        print("\n" + "Despesa adicionada com sucesso!")
        input("\n" + "Para prosseguir, pressione Enter")

    elif opcao == "2":
        print("\n" + "Listando as despesas abaixo: ")
        listar_despesas(despesas)
        input("\n" + "Para prosseguir, pressione Enter")
    elif opcao == "3": 
        print("\n" + "Saindo do programa")
        break
    else:
        print("\n" + "Opção inválida. Por favor, selecione uma opção válida.")
    