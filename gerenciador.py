"""
Módulo Gerenciador (Regra do negócio)
Responsável por registrar movimentações, calcular saldos, ordenar extratos
cronologicamente, filtrar despesas e remover lançamentos.
"""

# Importação das funções 

from datetime import datetime
from armazenamento import salvar_dados

# Funções

def registrar_movimentacao(lista, tipo, descricao, categoria, valor, data_br):
    """
    Cria um dicionário representando a movimentação, adiciona à lista
    e persiste imediatamente no arquivo JSON.
    """
    nova_movimentacao = {
        "tipo": tipo,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor, 
        "data": data_br,
    }
    lista.append(nova_movimentacao)
    salvar_dados(lista)

def calcular_resumo(lista):
    """
    Calcular o total de entrada, total de saída e o saldo atual.
    Retorna uma tupla: (total_entrada, total_saida, saldo).
    """
    total_entradas = sum (
        item["valor"] for item in lista if item["tipo"] == "entrada"
    )
    total_saidas = sum (
        item["valor"] for item in lista if item["tipo"] == "saida"
    )
    saldo = total_entradas - total_saidas
    return total_entradas, total_saidas, saldo

def obter_extrato_ordenado(lista):
    """
    Retorna uma nova lista com todas as movimentações ordenadas
    cronologicamente pela data no formato brasileiro (DD/MM/AAAA).
    """
    return sorted(
        lista,
        key=lambda item: datetime.strptime(item["data"], "%d/%m/%Y"),
    )

def lista_despesas_detalhadas(lista):
    """
    Filtra apenas as movimentações do tipo 'saída', ordena por data
    e calcula o valor total de gasto.
    Retorna uma tupla: (despesas_ordenadas, total_gastos). 
    """
    despesas = [item for item in lista if item["tipo"] == "saida"]
    despesas_ordenadas = obter_extrato_ordenado(despesas)
    total_gasto = sum(item["valor"] for item in despesas_ordenadas)
    return despesas_ordenadas, total_gasto

def remover_movimentacao(lista, indice_usuario):
    """
    Remove um lançamento com base no número exibido ao usuário (iniciando em 1)
    e atualiza o arquivo JSON.
    Retorna uma tupla: (sucesso: bool, item_removido: dict | None).
    """
    # Converte o número visual (1,2,3,...) para o índice real do Python (0,1,2,...)
    indice_real = indice_usuario - 1

    if 0 <= indice_real < len(lista):
        item_removido = lista.pop(indice_real)
        salvar_dados(lista)
        return True, item_removido

    return False, None 