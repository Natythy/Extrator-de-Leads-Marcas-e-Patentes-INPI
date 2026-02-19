import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os
import glob

# Configurações de caminhos (Ideal manter relativo para funcionar no GitHub de qualquer um)
PASTA_ENTRADA = os.path.join("data", "raw", "2016")
PASTA_SAIDA = os.path.join("data", "processed")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "leads_renovacao_marcas.xlsx")


def parse_data_inpi(data_str):
    """Converte string 'DD/MM/YYYY' para objeto datetime."""
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except (ValueError, TypeError):
        return None


def processar_xml(caminho_arquivo):
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()

    dados_extraidos = []

    # Itera sobre cada processo dentro da revista
    for processo in root.findall("processo"):

        # 1. Verifica se tem o despacho IPAS158 (Concessão de Registro)
        # O despacho pode estar aninhado, então verificamos a lista de despachos
        tem_ipas158 = False
        despachos = processo.find("despachos")
        if despachos is not None:
            for despacho in despachos.findall("despacho"):
                if despacho.get("codigo") == "IPAS158":
                    tem_ipas158 = True
                    break

        if not tem_ipas158:
            continue

        # 2. Extração de Titulares e Filtro de País (BR)
        titulares_node = processo.find("titulares")
        if titulares_node is None:
            continue

        # Pega o primeiro titular (geralmente é um só, mas o XML aceita lista)
        titular = titulares_node.find("titular")
        if titular is None:
            continue

        pais = titular.get("pais")
        if pais != "BR":
            continue

        # 3. Filtro de Data de Depósito (> 2010)
        data_deposito_str = processo.get("data-deposito")
        data_deposito_dt = parse_data_inpi(data_deposito_str)

        # Se não tiver data ou for anterior a 2011 (<= 2010), pula
        if not data_deposito_dt or data_deposito_dt.year <= 2010:
            continue

        # 4. Extração dos demais dados solicitados

        # Marca (Nome)
        nome_marca = "Mista/Figurativa" # Valor padrão caso não tenha texto
        marca_node = processo.find("marca")
        
        if marca_node is not None:
            # Tenta encontrar a tag <nome> dentro de <marca>
            nome_node = marca_node.find("nome")
            # Só acessa .text se nome_node existir E tiver conteúdo
            if nome_node is not None and nome_node.text:
                nome_marca = nome_node.text

        # Especificação (Serviços/Produtos)
        classe_nice = processo.find("classe-nice")
        especificacao = ""
        if classe_nice is not None:
            spec_node = classe_nice.find("especificacao")
            if spec_node is not None:
                especificacao = spec_node.text

        # Monta o dicionário da linha
        linha = {
            "Numero Processo": processo.get("numero"),
            "Marca": nome_marca,
            "Titular": titular.get("nome-razao-social"),
            "UF": titular.get("uf"),
            "Data Deposito": data_deposito_str,
            "Data Vigencia": processo.get("data-vigencia"),
            "Especificacao": especificacao.strip() if especificacao else "",
            "Codigo Despacho": "IPAS158"
        }

        dados_extraidos.append(linha)

    return dados_extraidos


def main():
    # Garante que a pasta de saída existe
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Lista todos os XMLs na pasta raw
    arquivos_xml = glob.glob(os.path.join(PASTA_ENTRADA, "*.xml"))
    print(f"Encontrados {len(arquivos_xml)} arquivos XML para processar.")

    todos_dados = []

    for arquivo in arquivos_xml:
        print(f"Processando: {os.path.basename(arquivo)}...")
        try:
            dados = processar_xml(arquivo)
            todos_dados.extend(dados)
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    # Cria o DataFrame e Exporta
    if todos_dados:
        df = pd.DataFrame(todos_dados)

        # Opcional: Ordenar por data de vigência para o cliente priorizar quem vai vencer logo
        # df.sort_values(by="Data Vigencia", inplace=True)

        print(f"Total de registros extraídos: {len(df)}")
        df.to_excel(ARQUIVO_SAIDA, index=False)
        print(f"Arquivo gerado com sucesso em: {ARQUIVO_SAIDA}")
    else:
        print("Nenhum registro encontrado com os filtros aplicados.")


if __name__ == "__main__":
    main()
