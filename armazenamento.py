
"""
Módulo de Armazenamento (Persistência de Dados)
Responsável por ler e gravar as moviemntações financeiras em arquivos JSON
e exportar relatórios em formato CSV.
"""

# Importação das bibliotecas necessárias

import json
import csv
import os

"""
Import json: usado para converter dados de python em formato JSON e vice-versa
Import csv: usado para ler e escrever arquivos CSV 
Import os: usado para interagir com o sistema operacional, como verificar a existência de arquivos
antes de tentar lê-los ou gravá-los.
"""

# Nome padrão do arquivo onde os dados serão persistidos

ARQUIVOS_DADOS = "dados.json"

# Funções

def carregar_dados():
    """
    Lê os dados .json e retorna a lista de movimentações.
    Se o arquivo ainda não existir ou estiver inválido, retorna uma lista vazia.
    """
    if not os.path.exists(ARQUIVOS_DADOS):
        return []

    try:
        with open(ARQUIVOS_DADOS, mode="r", encoding="utf-8") as arquivo: 
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print("\n[Aviso] Arquivo de dados vazio ou inválido. Iniciado lista vazia.")

def salvar_dados(lista_movimentacoes):
    """
    Grava a lista completa de movimentações no arquivo dados.json. 
    """
    with open(ARQUIVOS_DADOS, mode="w", encoding="utf-8") as arquivos:
        json.dump(lista_movimentacoes, arquivos, indent=4, ensure_ascii=False)

def exportar_para_csv(lista_movimentacoes, nome_arquivo="extrato_financeiro.csv"):
    """
    Exporta a lista de movimentações para um arquivo CSV compatível com Excel.
    """
    with open(nome_arquivo, mode="w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")

        # Escreve a primeira linha (cabeçario das colunas)
        escritor.writerow(["Data", "Tipo", "Descrição", "Categoria", "Valor"])

        # Percorre cada movimentação e escreve uma linha na planilha
        for item in lista_movimentacoes:
            valor_formatado = f"{item['valor']:.2f}".replace(".", ",")
            escritor.writerow([
                item["data"],
                item["tipo"].capitalize(),
                item["descricao"],
                item["categoria"],
                valor_formatado,
            ])