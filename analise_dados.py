import sqlite3

# Conecta com o Banco de Dados criado/existente
conn = sqlite3.connect('atendimentos.db')
cursor = conn.cursor()

print("- - - RELATÓRIO DE EFICIÊNCIA DE ATENDIMENTO - - -")

# Variável que conta os chamados por categoria,
# agrupa e ordena em ordem decrescente
query1 = '''
SELECT categoria, COUNT(*) as total
FROM chamados
GROUP BY categoria
ORDER BY total DESC;
'''

cursor.execute(query1)
print("1. Volume de Chamados por Categoria:")

# Retorna as linhas dos resultados da busca
for linha in cursor.fetchall():
    print(f" {linha[0]}: {linha[1]} chamados")
print("\n-----------------------------------------")

# Variável que calcula a média dos tempos de chamados por categoria,
# agrupa e ordena em ordem decrescente
query2 = '''
SELECT categoria, AVG(tempo_resposta_segundos) as media_segundos
FROM chamados
GROUP BY categoria
ORDER BY media_segundos DESC;
'''

cursor.execute(query2)
print("2. Tempo Médio de Resposta (Identificação de Lentidão):")

# Retorna as linhas dos resultados da busca
for linha in cursor.fetchall():
    categoria = linha[0]
    media = round(linha[1], 2)  # Média com valores arredondados

    alerta = ""
    if media > 100:
        alerta = "[ALERTA DE GARGALO]"

    print(f" {categoria}: {media} segundos {alerta}")

conn.close()
