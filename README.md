# 📊 Simulador de Análise de Gargalos

Projeto desenvolvido como **Prova de Conceito (PoC)** para demonstrar competências em Engenharia de Dados, Automação com Python, Integração de APIs e Análise SQL.

O objetivo foi simular um cenário real de atendimento ao cliente, gerar massa de dados, enriquecê-los com informações externas e identificar automaticamente ineficiências operacionais.

## 🚀 Tecnologias Utilizadas
* **Python 3**: Lógica de automação e manipulação de dados.
* **Requests**: Consumo de APIs REST para integração de sistemas.
* **SQLite**: Banco de dados relacional e evolução de schema (`DDL`).
* **SQL (Analytics)**: Uso de `GROUP BY`, `AVG`, `UPDATE` e `COUNT`.

## 🎯 O Problema de Negócio
Para otimizar uma operação de CX (Customer Experience), é necessário identificar onde estão os gargalos e entender o contexto (ex: feriados). Analisar planilhas manualmente é lento. O sistema precisa apontar automaticamente onde o tempo de resposta está acima do SLA (Service Level Agreement).

## 🛠 Como a Solução Funciona
O pipeline é dividido em três scripts autônomos:

### 1. Gerador de Cenários (`gerar_banco.py`)
Atua como um **Engine de Mock Data**. Ele cria um banco de dados SQLite e popula com 100 chamados fictícios.
* **Diferencial:** Implementei uma lógica probabilística que insere "vícios" nos dados (ex: a categoria 'Suporte Técnico' tem tempos de resposta propositalmente altos) para validar a eficácia da análise posterior.

### 2. Enriquecimento de Dados (`enriquecer_dados.py`) 🆕
Conecta o banco de dados local à internet para adicionar contexto.
* **Integração API:** Consome a **BrasilAPI** para buscar feriados nacionais.
* **Engenharia:** Executa uma migração de schema (`ALTER TABLE`) para criar novas colunas e utiliza lógica de sanitização (`SUBSTR`) para cruzar datas de formatos diferentes.

### 3. Analista de Dados (`analise_dados.py`)
Conecta ao banco e executa queries SQL para responder perguntas de negócio:
* **Volumetria:** Qual categoria tem mais chamados?
* **Eficiência:** Qual o tempo médio de cada área?
* **Alerta Inteligente:** O script possui uma camada lógica em Python que processa o resultado do SQL e dispara um `[ALERTA DE GARGALO]` visual caso a média ultrapasse 100 segundos.

## ⚙️ Como Executar
1. Clone este repositório.

2. Instale as dependências:
   ```bash
   pip install requests

3. Gere e enriqueça a massa de dados:
   ```bash
   python gerar_banco.py
   python enriquecer_dados.py

4. Execute a análise de performance:
   ```bash
   python analise_dados.py

📈 Exemplo de Saída (Terminal)

- - - RELATÓRIO DE EFICIÊNCIA DE ATENDIMENTO - - -
1. Volume de Chamados por Categoria:
 Vendas: 110 chamados
 Financeiro: 109 chamados
 Suporte Técnico: 92 chamados
 Dúvidas Gerais: 89 chamados

-----------------------------------------
2. Tempo Médio de Resposta (Identificação de Lentidão):
 Suporte Técnico: 351.41 segundos [ALERTA DE GARGALO]  
 Vendas: 34.75 segundos 
 Dúvidas Gerais: 33.7 segundos 
 Financeiro: 33.53 segundos