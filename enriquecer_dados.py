import sqlite3
import requests

print("--- INICIANDO ENRIQUECIMENTO ---")

url = "https://brasilapi.com.br/api/feriados/v1/2025"  # Feriados do Brasil

# Tenta conectar com API e caso não consiga, retorna lista vazia
try:
    print("1. Consultando API...")
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        feriados = response.json()  # Converte a resposta em JSON
        print(f"   Sucesso! {len(feriados)} feriados encontrados.")
    else:
        print("   Erro na resposta da API.")
        feriados = []
except Exception as e:
    print(f"   Erro de conexão: {e}")
    feriados = []

# Abre o banco de dados
conn = sqlite3.connect('atendimentos.db')
cursor = conn.cursor()

# Tenta criar uma linha nova para Feriados.
print("2. Atualizando banco de dados...")
try:
    cursor.execute("ALTER TABLE chamados ADD COLUMN eh_feriado TEXT")
except sqlite3.OperationalError:
    pass

# Limpa os dados antigos para inseção dos mais atuais
cursor.execute("UPDATE chamados SET eh_feriado = 'Não'")

registros_alterados = 0

# Compara os dados de feriados recebidos com as datas atuais
for item in feriados:
    data_feriado = item['date']  # Formato recebido da API: '2025-01-01'

    # Ajusta data do DB usando apenas a data e não a hora
    # por usar apenas 10 caracteres
    query = '''
        UPDATE chamados
        SET eh_feriado = 'Sim'
        WHERE SUBSTR(data_abertura, 1, 10) = ?
    '''

    # Vírgula após data_feriado classifica como uma tupla e evita erro
    cursor.execute(query, (data_feriado,))
    registros_alterados += cursor.rowcount

conn.commit()
conn.close()

print(f"3. Concluído! Total de chamados em feriados: {registros_alterados}")
