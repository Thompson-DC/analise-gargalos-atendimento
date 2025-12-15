import sqlite3
import random
from datetime import datetime, timedelta

# conectando db ficticio
conn = sqlite3.connect('atendimentos.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_abertura DATETIME,
    categoria TEXT,
    status TEXT,
    tempo_resposta_segundos INTEGER
    eh_feriado TEXT,
    comentario TEXT,
    sentimento_ia TEXT
)
''')

# Lista de valores sorteados
categorias = ['Financeiro', 'Suporte Técnico', 'Vendas', 'Dúvidas Gerais']
status_opcoes = ['Concluído', 'Pendente', 'Cancelado', 'Em Análise']

# Dados Simulados [MOCK DATA] com frases para testar a inteligência da IA
comentarios_mock = [
    "O atendimento foi excelente, resolveram tudo muito rápido!",
    "Péssimo serviço, fiquei esperando horas e ninguém atendeu.",
    "Gostaria de saber mais sobre os planos, mas o site estava lento.",
    "O suporte técnico foi muito atencioso e educado.",
    "Cobrança indevida na minha fatura, estou muito irritado!",
    "Só queria tirar uma dúvida simples, tudo ok.",
    "Não recomendo, experiência frustrante com a equipe de vendas.",
    "Amei o produto, chegou antes do prazo!",
    "Atendente mal preparado, não sabia responder nada.",
    "Processo burocrático demais para cancelar uma assinatura."
]

print('Gerando dados simulados...')

# Criação de 100 chamados em loop
for _ in range(100):
    categoria = random.choice(categorias)
    status = random.choice(status_opcoes)
    comentario = random.choice(comentarios_mock)  # Sorteia o comentário

    # Simulando realidade de categoria crítica em tempo de atendimento (Neste
    # exemplo será o "Suporte Técnico") para tomada de ação
    if categoria == 'Suporte Técnico':
        tempo = random.randint(120, 600)
    else:
        tempo = random.randint(10, 60)

    # Gera data aleatória nos ultimos 30 dias
    data = datetime.now() - timedelta(days=random.randint(0, 30))

    cursor.execute('''
        INSERT INTO chamados (
            data_abertura, categoria, status,
            tempo_resposta_segundos, comentario
        ) VALUES (?, ?, ?, ?, ?)
    ''', (data, categoria, status, tempo, comentario))

# Finaliza comando/Salva as alterações
conn.commit()

# Fecha o banco de dados
conn.close()
print("Banco de dados 'atendimentos.db' criado com 100 registros.")
