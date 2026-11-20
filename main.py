"""
Módulo principal (Interface CLI)
Gerencia o menu interativo no terminal, valida as entradas do usuário
e exibe extratos e relatórios financeiros.
"""

#Importação das funções

import os
from datetime import datetime
from armazenamento import carregar_dados, exportar_para_csv
from gerenciador import (
    calcular_resumo,
    lista_despesas_detalhadas,
    obter_extrato_ordenado,
    registrar_movimentacao,
    remover_movimentacao,
)

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

def obter_data_hoje_br():    
    """
    Retorna a data atual do sistema no formato brasileiro DD/MM/AAAA.
    """
    return datetime.now().strftime("%d/%m/%Y")

def formatar_moeda(valor):
    """
    Formata um float para padrão visual brasileiro (ex: 1250.50 para '1.250,50')
    """
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def iniciar_sistema ():
    """
    Carregar os dados e executa o loop principal do menu CLI
    """
    movimentacoes = carregar_dados()

    while True:

        limpar_tela()

        print("\n=== RASTREADOR DE DESPESA & FLUXO DE CAIXA v2.0 ===")
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
            data_br = obter_data_hoje_br()

            registrar_movimentacao(movimentacoes, tipo, descricao, categoria, valor, data_br)

            print(f"\n[SUCESSO] {titulo_acao.capitalize()} registrada na data {data_br}")

        # Exibição do extrato consolidado em ordem cronológica 
        elif opcao == "3":

            entradas, saidas, saldo = calcular_resumo(movimentacoes)
            extrato = obter_extrato_ordenado(movimentacoes)

            print("\n" + "=" *40)
            print("EXTRATO FINANCEIRO".center(40))
            print("=" *40)
            print()
            print(f"Total De Entradas: R$ {formatar_moeda(entradas)}")
            print(f"Total De Saídas:   R$ {formatar_moeda(saidas)}")
            print(f"Saldo Atual:       R$ {formatar_moeda(saldo)}")
            print("\n" + "-" *30)

            if not extrato:
                print("Nenhuma movimentação registrada!")

            else:
                for indice, item in enumerate(extrato, start=1):
                    sinal = "[+]" if item["tipo"] == "entrada" else "[-]"
                    print()
                    print (
                        f"{indice}. {item['data']} | {sinal} {item['descricao']} "
                        f"({item['categoria']}) - R$ {formatar_moeda(item['valor'])}"
                    )
            print("\n" + "=" *30)

        # Relatório filtrado apenas com gastos
        elif opcao == "4":

            despesas, total_gasto = lista_despesas_detalhadas(movimentacoes)

            print("\n--- Relatório De Despesas ---")

            if not despesas:
                print("\nNenhuma despesa cadastrada")
            
            else:
                for indice, item in enumerate(despesas, start=1):
                    print()
                    print(
                        f"{indice}. {item['data']} | {item['descricao']} "
                        f"({item['categoria']}) - R$ {formatar_moeda(item['valor'])}"
                    )

                print("\n" + "-" *30)
                print(f"TOTAL DE GASTO: R$ {formatar_moeda(total_gasto)}")

        # Remoção de item específico por índice visual
        elif opcao == "5":

            if not movimentacoes:
                print("\nNenhum lançamento disponível para remover!")
                input("\nPressione Enter para voltar ao menu")
                continue

            print("\n--- REMOVER LANÇAMENTO ---")
            print()

            for indice, item in enumerate(movimentacoes, start=1):
                print(
                    f"{indice}. {item['data']} | {item['descricao']} "
                    f"- R$ {formatar_moeda(item['valor'])}"
                )

            try:
                numero = int(input("\nDigite o número para remover (0 para cancelar): "))
                print()

                if numero == 0:
                    print("Operação cancelada")

                else:
                    sucesso, removido = remover_movimentacao(movimentacoes, numero)

                    if sucesso:
                        print(f"[Sucesso] '{removido['descricao']}' removido!")

                    else:
                        print("[Erro] Número inválido.")

            except ValueError:

                print("[Erro] Digite apenas o número correspondente ao item.")

        # Geração do arquivo CSV para abertura no Excel 
        elif opcao == "6":

            if not movimentacoes:
                print("\nNão há dados para exportar!")
                input("\nPressione Enter para voltar ao menu")
                continue

            extrato_ordenado = obter_extrato_ordenado(movimentacoes)
            exportar_para_csv(extrato_ordenado)

            print("[Sucesso] Arquivo 'extrato_financeiro.csv' gerado na pasta do projeto!")

        # Encerramento do loop principal
        elif opcao == "7":

            print("\nEncerrando o sistema. Até logo!")
            print()

            break

        else:

            print("[Erro] Digite uma opção válida! Escolha um número de 1 a 7.")

        # Pausa a execução após qualquer opção (Exceto '7', que utiliza o break)
        input("\nPressione Enter para voltar ao menu")

# Garante que o menu só seja executado quando este arquivo for rodado diretamente
if __name__ == "__main__":
    iniciar_sistema()