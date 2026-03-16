import pandas as pd
from faker import Faker
import argparse
import random
from datetime import datetime, timedelta

def generate_data(rows, types, start_date=None, end_date=None):
    fake = Faker('pt_BR')
    data = {}
    
    # Produtos fictícios para vendas
    produtos = [
        "Smartphone Samsung Galaxy", "iPhone 15 Pro", "Notebook Dell Inspiron", 
        "Monitor LG 27\"", "Teclado Mecânico RGB", "Mouse Gamer Logitech", 
        "Fone de Ouvido Sony WH", "Cadeira Gamer", "Mesa de Escritório", 
        "Impressora HP Laser", "Tablet iPad Air", "Smartwatch Apple Watch"
    ]
    
    mapping = {
        'nome': fake.name,
        'email': fake.email,
        'telefone': fake.phone_number,
        'endereco': fake.address,
        'profissao': fake.job,
        'empresa': fake.company,
        'data': lambda: fake.date_between(start_date=start_date or '-1y', end_date=end_date or 'today'),
        'texto': fake.text,
        'cpf': fake.cpf,
        'cidade': fake.city,
        'estado': fake.state_abbr,
        'cep': fake.postcode,
        # Novos campos de vendas
        'produto': lambda: random.choice(produtos),
        'quantidade': lambda: random.randint(1, 5),
        'valor_unitario': lambda: round(random.uniform(50.0, 5000.0), 2),
        'categoria': lambda: random.choice(["Eletrônicos", "Informática", "Móveis", "Acessórios"])
    }
    
    for t in types:
        if t in mapping:
            col_name = t.replace('_', ' ').capitalize()
            data[col_name] = [mapping[t]() for _ in range(rows)]
        else:
            print(f"Aviso: Tipo de dado '{t}' não reconhecido. Pulando.")
    
    # Se tivermos valor e quantidade, podemos criar o Total
    if 'Valor unitario' in data and 'Quantidade' in data:
        data['Total'] = [round(float(q) * float(v), 2) for q, v in zip(data['Quantidade'], data['Valor unitario'])]
    
    df = pd.DataFrame(data)
    
    # Se tiver data, podemos extrair dia, semana, mês e ano
    if 'Data' in data:
        df['Data'] = pd.to_datetime(df['Data'])
        df['Dia'] = df['Data'].dt.day
        df['Semana'] = df['Data'].dt.isocalendar().week
        df['Mes'] = df['Data'].dt.month
        df['Ano'] = df['Data'].dt.year
        
        # Adiciona o nome do mês
        meses_map = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        df['Nome do Mês'] = df['Mes'].map(meses_map)
        
        # Deixamos como datetime internamente para facilitar exportação, 
        # mas no CSV/XLSX o pandas cuidará da formatação
        
    return df

def main():
    parser = argparse.ArgumentParser(description="Gerador de planilha de dados fictícios")
    parser.add_argument("-r", "--rows", type=int, default=10, help="Quantidade de linhas a gerar")
    parser.add_argument("-t", "--types", nargs="+", default=['nome', 'email', 'telefone'], 
                        help="Tipos de dados (ex: nome email telefone endereco profissao empresa data texto cpf cidade estado cep produto quantidade valor_unitario categoria)")
    parser.add_argument("-o", "--output", type=str, default="dados_ficticios.csv", help="Nome do arquivo de saída")
    
    args = parser.parse_args()
    
    print(f"Gerando {args.rows} linhas com os tipos: {', '.join(args.types)}...")
    df = generate_data(args.rows, args.types)
    
    if args.output.endswith('.xlsx'):
        df.to_excel(args.output, index=False)
    else:
        df.to_csv(args.output, index=False, encoding='utf-8-sig', decimal=',')
    print(f"Arquivo '{args.output}' gerado com sucesso!")

if __name__ == "__main__":
    main()
