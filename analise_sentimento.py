import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# 1. Lê o arquivo .env com segurança
load_dotenv()

# 2. Configura a API do Google
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERRO CRÍTICO: Chave API não encontrada. Verifique o arquivo .env")
    exit()

genai.configure(api_key=api_key)

# 3. Configura o Modelo (Determinístico)
# Temperatura 0 para tirar a criatividade da IA, deixando-a Analítica.
model = genai.GenerativeModel(
    model_name="gemma-3-1b-it",
    generation_config={"temperature": 0}
)

conn = sqlite3.connect('atendimentos.db')
cursor = conn.cursor()

# 4. Busca apenas o trabalho pendente
cursor.execute('''
    SELECT
        id,
        comentario
    FROM chamados
    WHERE sentimento_ia IS NULL
''')

fila_de_trabalho = cursor.fetchall()

print(f"Iniciando análise de IA em {len(fila_de_trabalho)} registros...")

contador = 0

for chamado in fila_de_trabalho:
    id_chamado = chamado[0]
    texto_comentario = chamado[1]

    # Engenharia de Prompt
    prompt = f'''
    Aja como especialista em Experiência do Cliente.
    Analise o comentário abaixo e clasifique o sentimento.
    Regra: Responda APENAS uma das palavras: Positivo, Negativo ou Neutro.

    Comentário : "{texto_comentario}"
    '''

    # Loop de tentativas. Tenta processar até falhar
    while True:
        try:
            print(f"Processando ID {id_chamado}...", end=" ", flush=True)

            # Chama IA
            response = model.generate_content(prompt)
            sentimento = response.text.strip()  # Limpa espaços da resposta
            sentimento = sentimento.replace("**", "").replace("Sentimento:", "").strip()
            query = '''
                UPDATE chamados
                SET sentimento_ia = ?
                WHERE id = ?
            '''
            cursor.execute(query, (sentimento, id_chamado))
            conn.commit()  # Salva a linha para não perder progresso se cair

            print(f"-> {sentimento}")
            contador += 1

            # Rate Limiting
            time.sleep(2)
            break

        except Exception as e:
            erro_str = str(e)
            # Se for erro de Cota (429), ativamos o modo "Espera Longa"
            if "429" in erro_str:
                print("\n[COTA EXCEDIDA] Pausando a anpalise por 60 segundos")
                time.sleep(60)
                print("Retomando...")
            else:
                print(f"\nERRO no ID: {id_chamado}: {e}")
                break

conn.close()
print("\n--- FIM ---")
print(f"\nSucesso! {contador} comentários foram analisados pela IA.")
