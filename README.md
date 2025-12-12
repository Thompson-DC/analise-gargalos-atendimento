# 📊 Simulador de Análise de Gargalos

Projeto desenvolvido como **Prova de Conceito (PoC)** para demonstrar competências em Engenharia de Dados, Automação com Python e Análise SQL.

O objetivo foi simular um cenário real de atendimento ao cliente, gerar massa de dados e identificar automaticamente ineficiências operacionais.

## 🚀 Tecnologias Utilizadas
* **Python 3**: Lógica de automação e manipulação de dados.
* **SQLite**: Banco de dados relacional para persistência das transações.
* **SQL (Analytics)**: Uso de `GROUP BY`, `AVG` e `COUNT` para extração de KPIs.

## 🎯 O Problema de Negócio
Para otimizar uma operação de CX (Customer Experience), é necessário identificar onde estão os gargalos. Analisar planilhas manualmente é lento. O sistema precisa apontar automaticamente onde o tempo de resposta está acima do SLA (Service Level Agreement).

## 🛠 Como a Solução Funciona
O projeto é dividido em dois scripts autônomos:

### 1. Gerador de Cenários (`gerar_banco.py`)
Atua como um **Engine de Mock Data**. Ele cria um banco de dados SQLite e popula com 100 chamados fictícios.
* **Diferencial:** Implementei uma lógica probabilística que insere "vícios" nos dados (ex: a categoria 'Suporte Técnico' tem tempos de resposta propositalmente altos) para validar a eficácia da análise posterior.

### 2. Analista de Dados (`analise_dados.py`)
Conecta ao banco e executa queries SQL para responder perguntas de negócio:
* **Volumetria:** Qual categoria tem mais chamados?
* **Eficiência:** Qual o tempo médio de cada área?
* **Alerta Inteligente:** O script possui uma camada lógica em Python que processa o resultado do SQL e dispara um `[ALERTA DE GARGALO]` visual caso a média ultrapasse 100 segundos.

## ⚙️ Como Executar
1. Clone este repositório.
2. Gere o banco de dados simulado:
   ```bash
   python gerar_banco.py
3. Execute a análise de performance:
   ```bash
   python analise_dados.py


## 📈 Exemplo de Saída (Terminal)
```text
2. Tempo Médio de Resposta (Identificação de Lentidão):
   Suporte Técnico: 345.20 segundos [ALERTA DE GARGALO] ⚠️
   Financeiro: 42.10 segundos
   Vendas: 38.50 segundos   

Autor: Thompson Carvalho - Estudante de Análise e Desenvolvimento de Sistemas