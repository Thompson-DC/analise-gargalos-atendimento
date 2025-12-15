import sqlite3

# Conecta no banco
conn = sqlite3.connect('atendimentos.db')
cursor = conn.cursor()

# Executa a auditoria
print("--- AUDITORIA DE DADOS ---")
print("Verificando distribuição dos sentimentos...")

try:
    cursor.execute('''
        SELECT sentimento_ia,
        COUNT(*)
        FROM chamados
        GROUP BY sentimento_ia;
    ''')
    resultados = cursor.fetchall()

    print(f"{'SENTIMENTO':<15} | {'QUANTIDADE':<10}")
    print("-" * 30)

    total = 0
    for linha in resultados:
        sentimento = linha[0]
        qtd = linha[1]
        # Se sentimento for None, mostra como 'NULO'
        if sentimento is None:
            sentimento = "NULO (Erro)"

        print(f"{sentimento:<15} | {qtd:<10}")
        total += qtd

    print("-" * 30)
    print(f"TOTAL REGISTROS: {total}")

except Exception as e:
    print(f"Erro ao ler banco: {e}")

conn.close()
