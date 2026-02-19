# 📥 Extrator de Leads: Marcas e Patentes (INPI)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/managed%20by-uv-arc.svg)](https://github.com/astral-sh/uv)
[![Pandas](https://img.shields.io/badge/Library-Pandas-150458.svg)](https://pandas.pydata.org/)

## 📝 Sobre o Projeto
Este projeto foi desenvolvido para resolver um problema real de prospecção de vendas. Ele realiza o **ETL (Extract, Transform, Load)** de bases de dados abertas do INPI (Instituto Nacional da Propriedade Industrial), extraindo empresas que tiveram marcas concedidas e estão próximas do período de renovação.

O pipeline processa grandes volumes de arquivos XML, aplica filtros de regras de negócio e gera uma lista qualificada de leads em formato Excel.

### 🎯 Resultados Obtidos
- **Processamento em Lote:** 52 arquivos XML processados simultaneamente.
- **Volume de Dados:** +65.000 registros extraídos e tratados.
- **Filtros Aplicados:** - Somente concessões (Código IPAS158).
  - Somente empresas brasileiras (País BR).
  - Filtro temporal (Depósitos - Quando o pedido de registro foi iniciado) pós-2010.

## 🛠️ Tecnologias e Ferramentas
- **[uv](https://github.com/astral-sh/uv):** Gerenciador de pacotes e ambientes Python de alta performance.
- **Pandas:** Manipulação de dados e exportação para Excel.
- **XML ElementTree:** Parsing eficiente de arquivos hierárquicos complexos.
- **Pathlib:** Gerenciamento de caminhos agnóstico ao sistema operacional.

## 📁 Estrutura do Projeto
```text
├── data/
│   ├── raw/          # XMLs brutos (não inclusos no Git)
│   └── processed/    # Planilhas geradas (leads_renovacao_marcas.xlsx)
├── src/
│   └── processar_marcas.py  # Script principal de ETL
├── pyproject.toml    # Configuração do projeto e dependências
└── README.md
```

## 🚀 Como Rodar

1. Certifique-se de ter o uv instalado.
2. Clone o repositório.
3. Coloque os XMLs do INPI na pasta data/raw/.
4. Execute o comando:

``` bash
uv run src/processar_marcas.py
```

## 📈 Próximos Passos

* [ ] Implementar Crawler para busca automática de e-mails/telefones via CNPJ.
* [ ] Adicionar suporte a banco de dados SQLite para histórico de leads.
* [ ] Criar dashboard em Streamlit para visualização geográfica dos leads por UF.

**Desenvolvido por Nathaly Silva - Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/nathaly-silva01/)**