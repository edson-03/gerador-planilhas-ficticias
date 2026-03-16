import pandas as pd
from faker import Faker
import argparse
import random
from datetime import datetime, timedelta

def generate_data(rows, types, start_date=None, end_date=None):
    fake = Faker('pt_BR')
    data = {}
    
    # Pool de produtos vinculados às suas categorias corretas
    vendas_pool = [
        ("Smartphone Samsung Galaxy", "Eletrônicos"),
        ("iPhone 15 Pro", "Eletrônicos"),
        ("Notebook Dell Inspiron", "Informática"),
        ("Monitor LG 27\"", "Informática"),
        ("Teclado Mecânico RGB", "Acessórios"),
        ("Mouse Gamer Logitech", "Acessórios"),
        ("Fone de Ouvido Sony WH", "Acessórios"),
        ("Cadeira Gamer", "Móveis"),
        ("Mesa de Escritório", "Móveis"),
        ("Impressora HP Laser", "Informática"),
        ("Tablet iPad Air", "Eletrônicos"),
        ("Smartwatch Apple Watch", "Eletrônicos")
    ]
    
    # Mapa de meses para nome por extenso
    meses_map = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    # Se qualquer campo de tempo for solicitado, geramos as datas primeiro
    tempo_fields = {'data', 'dia', 'mes', 'ano', 'nome_mes', 'semana'}
    if any(f in types for f in tempo_fields):
        dates = [fake.date_between(start_date=start_date or '-1y', end_date=end_date or 'today') for _ in range(rows)]
        dates_dt = pd.to_datetime(dates)
        
        if 'data' in types: data['Data'] = dates_dt.strftime('%Y-%m-%d')
        if 'dia' in types: data['Dia'] = dates_dt.day
        if 'mes' in types: data['Mes'] = dates_dt.month
        if 'ano' in types: data['Ano'] = dates_dt.year
        if 'nome_mes' in types: data['Nome do Mês'] = dates_dt.month.map(meses_map)
        if 'semana' in types: data['Semana'] = dates_dt.isocalendar().week

    # Se 'produto' ou 'categoria' forem solicitados, sorteamos do pool de vendas
    if 'produto' in types or 'categoria' in types:
        selections = [random.choice(vendas_pool) for _ in range(rows)]
        if 'produto' in types: data['Produto'] = [s[0] for s in selections]
        if 'categoria' in types: data['Categoria'] = [s[1] for s in selections]

    # Se 'total' for solicitado, precisamos garantir que quantidade e valor_unitario existam
    if 'total' in types:
        if 'quantidade' not in types: types.append('quantidade')
        if 'valor_unitario' not in types: types.append('valor_unitario')

    mapping = {
        'nome': fake.name,
        'email': fake.email,
        'telefone': fake.phone_number,
        'endereco': fake.address,
        'profissao': fake.job,
        'empresa': fake.company,
        'texto': fake.text,
        'cpf': fake.cpf,
        'cidade': fake.city,
        'estado': fake.state_abbr,
        'cep': fake.postcode,
        'quantidade': lambda: random.randint(1, 5),
        'valor_unitario': lambda: round(random.uniform(50.0, 5000.0), 2)
    }
    
    for t in types:
        if t in mapping:
            col_name = t.replace('_', ' ').capitalize()
            # Evita sobrescrever se já geramos algo (como no caso de tempo ou produtos)
            if col_name not in data:
                data[col_name] = [mapping[t]() for _ in range(rows)]
    
    # Cálculo do Total (apenas se solicitado)
    if 'total' in types:
        data['Total'] = [round(float(q) * float(v), 2) for q, v in zip(data['Quantidade'], data['Valor unitario'])]
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="Gerador de planilha de dados fictícios")
    parser.add_argument("-r", "--rows", type=int, default=10, help="Quantidade de linhas a gerar")
    parser.add_argument("-t", "--types", nargs="+", default=['nome', 'email', 'telefone'], 
                        help="Tipos de dados")
    parser.add_argument("-o", "--output", type=str, default="dados_ficticios.csv", help="Nome do arquivo de saída")
    
    args = parser.parse_args()
    
    print(f"Gerando {args.rows} linhas...")
    df = generate_data(args.rows, args.types)
    
    if args.output.endswith('.xlsx'):
        df.to_excel(args.output, index=False)
    else:
        df.to_csv(args.output, index=False, encoding='utf-8-sig', decimal=',')
    print(f"Arquivo '{args.output}' gerado com sucesso!")

if __name__ == "__main__":
    main()
