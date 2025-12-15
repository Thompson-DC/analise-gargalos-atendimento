# 🤖 Pipeline de Dados com IA & Análise de Gargalos

Projeto desenvolvido como **Prova de Conceito (PoC)** para demonstrar competências em Engenharia de Dados, Automação com Python, Integração de APIs e Inteligência Artificial Generativa (LLMs).

O objetivo é simular um ecossistema de atendimento ao cliente, onde dados são gerados, enriquecidos com contexto externo (Feriados) e submetidos a uma análise de sentimento automática via IA para identificar ineficiências.

## 🚀 Tecnologias Utilizadas
* **Python 3**: Linguagem principal.
* **Google Generative AI (Gemma)**: Uso de LLMs para processamento de linguagem natural (NLP).
* **SQLite**: Banco de dados relacional para persistência.
* **Requests**: Integração com APIs REST públicas.
* **Dotenv**: Gestão de variáveis de ambiente e segurança.
* **SQL**: Consultas analíticas (`GROUP BY`, `AVG`) e DDL.

## 🛠 Arquitetura da Solução
O pipeline é dividido em etapas modulares de ETL (Extract, Transform, Load):

### 1. Ingestão de Dados (`gerar_banco.py`)
Atua como um **Mock Engine**. Cria um banco SQLite e popula com 100 chamados fictícios, inserindo propositalmente gargalos em categorias específicas para validar a análise.

### 2. Enriquecimento (`enriquecer_dados.py`)
Conecta o banco à **BrasilAPI** para identificar se a data de abertura do chamado foi um feriado nacional, adicionando contexto para justificar possíveis atrasos.

### 3. Inteligência Artificial (`analise_sentimento.py`) 🧠
O coração do projeto. Um script que lê os comentários dos clientes e utiliza o modelo **Gemma-3-1b-it** (via Google AI Studio) para classificar o sentimento como *Positivo*, *Negativo* ou *Neutro*.

* **Destaque Técnico (Engenharia de Performance):** Inicialmente testado com o modelo `Gemma-12b`, o pipeline apresentou latência alta (~49s/registro). Foi aplicada uma otimização de **Model Sizing**, migrando para a versão quantizada `Gemma-1b`, reduzindo o tempo de inferência para **~4s/registro** (92% de ganho) sem perda de precisão na tarefa.

### 4. Análise & QA (`analise_dados.py` e `verificar_banco.py`)
Scripts finais que geram KPIs de negócio (Tempo Médio de Resposta) e auditam a distribuição dos sentimentos no banco.

## ⚙️ Como Executar

1. **Clone o repositório:**
   ```bash
   git clone [URL_DO_SEU_REPO]

2. **Configure o Ambiente: Crie um arquivo .env na raiz do projeto e adicione sua chave:**
   GEMINI_API_KEY=Sua_Chave_Aqui

3. **Instale as dependências:**
   ```bash
   pip install requests google-generativeai python-dotenv

4. **Execute o Pipeline (Ordem Lógica):**
   ```bash
   # 1. Gerar massa de dados
      python gerar_banco.py

   # 2. Enriquecer com feriados
      python enriquecer_dados.py

   # 3. Classificar sentimentos com IA
      python analise_sentimento.py

   # 4. Gerar Relatórios
      python analise_dados.py

## 📈 Resultados Esperados
O sistema identificará automaticamente categorias com gargalos (ex: "Suporte Técnico") e classificará a satisfação dos clientes, permitindo uma visão 360º da operação.