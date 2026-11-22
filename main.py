"""
Módulo principal (Interface CLI)
Gerencia o menu interativo no terminal, valida as entradas do usuário
e exibe extratos e relatórios financeiros.
"""

#Importação das funções

import os
from gerenciador import (
    preparar_sistema,
    registrar_movimentacao,
    obter_resumo,
    extrato_completo,
    relatorio_despesa,
    remover_movimentacoes
)
from armazenamento import exportar_para_csv

# Funções

def limpar_tela():
    """
    Limpa o terminal (utilizando o 'cls' no Windows e 'clear' no Linux/Mac).
    """
    os.system("cls" if os.name == "nt" else "clear")

def ler_valor_valido(mensagem):
    """
    Solicita um valor monetário ao usuário, e converte vírgula em ponto 
    automaticamente e garante que seja um número maior que zero.
    """
    while True:

        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor > 0:
                return valor
            print("[Erro] O valor deve ser maior que 0.")
        except ValueError:
            print("[Erro] Valor inválido. Digite apenas números (ex: 45,90 ou 45.90)")

def ler_inteiro_valido(mensagem):
    """
    Não permite o usuário de digitar um número quebrado
    """
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("[Erro] Digite apenas um número inteiro válido")

def iniciar_sistema ():
    """
    Carregar os dados e executa o loop principal do menu CLI
    """
    preparar_sistema()

    while True:

        limpar_tela()

        print("\n=== RASTREADOR DE DESPESA & FLUXO DE CAIXA v3.0 ===")
        print("\n---      Persistência: SQLite (financas.db)     ---")
        print()
        print("1 - Registrar Entrada")
        print("2 - Registrar Despesa")
        print("3 - Ver Extrato Completo")
        print("4 - Ver Relatório de Despesa")
        print("5 - Remover Lançamento")
        print("6 - Exportar Extrato Para CSV")
        print("7 - Sair")
        print()

        opcao = input("Oque você deseja fazer hoje? ").strip()

        # Cadastro unificado para Entradas (1) e Despesas (2)
        if opcao in ("1", "2"):

            limpar_tela()

            tipo = "entrada" if opcao == "1" else "saida"
            titulo_acao = "ENTRADA" if tipo == "entrada" else "DESPESA"

            print(f"\n=== NOVO REGISTRO DE {titulo_acao} ===")
            print()

            descricao = input("Descrição: ").strip().title()
            categoria = input("Categoria: ").strip().title()

            # Impede registros com texto em branco
            if not descricao or not categoria:
                print("[ERRO] Descrição e categoria não podem ficar vazias")
                input("\nPressione Enter para voltar ao menu")
                continue

            valor = ler_valor_valido("Valor (R$): ")

            data_registrada = registrar_movimentacao(tipo, descricao, categoria, valor)

            print(f"\n[SUCESSO] {titulo_acao.capitalize()} registrada no banco de dados na data de {data_registrada}")

        # Exibição do extrato consolidado em ordem cronológica 
        elif opcao == "3":

            limpar_tela()

            entradas, saidas, saldo = obter_resumo()
            extrato = extrato_completo()

            print("\n" + "=" *60)
            print("EXTRATO FINANCEIRO".center(60))
            print("=" *60)
            print()
            print(f"Total De Entradas: R$ {entradas:.2f}")
            print(f"Total De Saídas:   R$ {saidas:.2f}")
            print(f"Saldo Atual:       R$ {saldo:.2f}")
            print("\n" + "-" *60)

            if not extrato:
                print("Nenhuma movimentação registrada no banco de dados!")

            else:
                print("\nEXTRATO CRONOLÓGICO:")
                for item in extrato:
                    sinal = "[+]" if item["tipo"] == "entrada" else "[-]"
                    print()
                    print (
                        f"[ID {item['id']}] {item['data_br']} | {sinal} "
                        f"{item['descricao']} ({item['categoria']}) - R$ {item['valor']:.2f}"
                    )
            print("\n" + "=" *60)

        # Relatório filtrado apenas com gastos
        elif opcao == "4":

            limpar_tela()

            despesas, total_gasto = relatorio_despesa()

            print("\n--- Relatório De Despesas ---")

            if not despesas:
                print("\nNenhuma despesa cadastrada")
            
            else:
                for item in despesas:
                    print()
                    print(
                        f"[ID {item ['id']}] {item['data_br']} | "
                        f"{item['descricao']} ({item['categoria']}) - R$ {item['valor']:.2f}"
                    )

                print("\n" + "-" *60)
                print()
                print(f"TOTAL DE GASTO: R$ {total_gasto:.2f}")

        # Remoção de item específico por índice visual
        elif opcao == "5":

            limpar_tela()

            extrato = extrato_completo()

            if not extrato:
                print("\nNenhum lançamento disponível para remover!")
                input("\nPressione Enter para voltar ao menu")
                continue

            print("\n--- REMOVER LANÇAMENTO ---")
            print()

            for item in extrato:
                print(
                    f"[ID {item['id']}] {item['data_br']} | "
                    f"{item['descricao']} - R$ {item['valor']:.2f}"
                )

                id_alvo = ler_inteiro_valido("\nDigite o ID do lançamento para excluir (Caso deseje cancelar, aperte 0):") 
                
                if id_alvo != 0:
                    if remover_movimentacoes(id_alvo):
                        print("\nRegistro ID {id_alvo} removido permanentemente do banco de dados!")

                    else:
                        print("\nNenhum registro encontrado com o ID {id_alvo}.")

        # Geração do arquivo CSV para abertura no Excel 
        elif opcao == "6":

            limpar_tela()

            extrato = extrato_completo()

            if not extrato:
                print("\nNão há dados para exportar!")
                input("\nPressione Enter para voltar ao menu")
                continue

            exportar_para_csv(extrato)

            print("[Sucesso] Arquivo 'extrato_financeiro.csv' gerado!")

        # Encerramento do loop principal
        elif opcao == "7":

            print("\nEncerrando o sistema. Até logo!")
            print()

            break

        else:

            print("[Erro] Digite uma opção válida! Escolha um número de 1 a 7.")

        # Pausa a execução após qualquer opção (Exceto '7', que utiliza o break)
        input("\nPressione Enter para voltar ao menu ")

# Garante que o menu só seja executado quando este arquivo for rodado diretamente
if __name__ == "__main__":
    iniciar_sistema()