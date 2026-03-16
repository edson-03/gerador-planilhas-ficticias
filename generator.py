import pandas as pd
from faker import Faker
import argparse
import random
import string
from datetime import datetime, timedelta

def generate_data(rows, types, start_date=None, end_date=None, company_name=None):
    fake = Faker('pt_BR')
    data = {}
    
    # Pool de produtos com categorias e faixas de preço inteligentes
    vendas_config = {
        "Eletrônicos": {
            "produtos": ["Smartphone Samsung Galaxy", "iPhone 15 Pro", "Tablet iPad Air", "Smartwatch Apple Watch"],
            "preço_min": 1500.0, "preço_max": 9000.0
        },
        "Informática": {
            "produtos": ["Notebook Dell Inspiron", "Monitor LG 27\"", "Impressora HP Laser"],
            "preço_min": 800.0, "preço_max": 5000.0
        },
        "Acessórios": {
            "produtos": ["Teclado Mecânico RGB", "Mouse Gamer Logitech", "Fone de Ouvido Sony WH"],
            "preço_min": 100.0, "preço_max": 1200.0
        },
        "Móveis": {
            "produtos": ["Cadeira Gamer", "Mesa de Escritório"],
            "preço_min": 400.0, "preço_max": 2500.0
        }
    }
    
    # Mapeamento de Cidades por Estado (Exemplos reais para consistência)
    geo_map = {
        "SP": ["São Paulo", "Campinas", "Santos", "Ribeirão Preto"],
        "RJ": ["Rio de Janeiro", "Niterói", "Búzios", "Petrópolis"],
        "MG": ["Belo Horizonte", "Uberlândia", "Ouro Preto", "Tiradentes"],
        "PR": ["Curitiba", "Londrina", "Foz do Iguaçu"],
        "RS": ["Porto Alegre", "Gramado", "Caxias do Sul"],
        "SC": ["Florianópolis", "Joinville", "Blumenau"],
        "BA": ["Salvador", "Porto Seguro", "Ilhéus"],
        "PE": ["Recife", "Olinda", "Caruaru"],
        "CE": ["Fortaleza", "Jericoacoara"],
        "DF": ["Brasília"]
    }
    
    # Mapa de meses para nome por extenso
    meses_map = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    # 1. Geração de Tempo
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

    # 2. Geração de Geografia (Consistência Estado -> Cidade)
    if 'estado' in types or 'cidade' in types:
        estados_disponiveis = list(geo_map.keys())
        estados_gerados = [random.choice(estados_disponiveis) for _ in range(rows)]
        if 'estado' in types: data['Estado'] = estados_gerados
        if 'cidade' in types: data['Cidade'] = [random.choice(geo_map[est]) for est in estados_gerados]

    # 3. Geração de Vendas Inteligente
    vendas_fields = {'produto', 'categoria', 'sku', 'valor_unitario'}
    if any(f in types for f in vendas_fields):
        categorias_disponiveis = list(vendas_config.keys())
        res_produtos, res_categorias, res_precos, res_skus = [], [], [], []
        
        for _ in range(rows):
            cat = random.choice(categorias_disponiveis)
            prod = random.choice(vendas_config[cat]["produtos"])
            preco = round(random.uniform(vendas_config[cat]["preço_min"], vendas_config[cat]["preço_max"]), 2)
            sku = f"{prod[:3].upper()}-{random.randint(100, 999)}"
            
            res_produtos.append(prod)
            res_categorias.append(cat)
            res_precos.append(preco)
            res_skus.append(sku)
            
        if 'produto' in types: data['Produto'] = res_produtos
        if 'categoria' in types: data['Categoria'] = res_categorias
        if 'valor_unitario' in types: data['Valor unitario'] = res_precos
        if 'sku' in types: data['SKU'] = res_skus

    # 4. Outros Campos Dinâmicos (Faker e Lógica)
    mapping = {
        'nome': fake.name,
        'email': fake.email,
        'telefone': fake.phone_number,
        'endereco': fake.address,
        'profissao': fake.job,
        'empresa': lambda: company_name if company_name else fake.company(),
        'texto': fake.text,
        'cpf': fake.cpf,
        'cnpj': fake.cnpj,
        'rg': lambda: f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(0, 9)}",
        'cep': fake.postcode,
        'vendedor': fake.name,
        'quantidade': lambda: random.randint(1, 5),
        'id_pedido': lambda: f"ORD-{random.randint(10000, 99999)}",
        'status': lambda: random.choice(["Pago", "Pendente", "Cancelado", "Em Processamento"])
    }
    
    # Preenche campos que ainda não foram preenchidos (evita sobrescrever geografia/vendas)
    for t in types:
        col_name = t.replace('_', ' ').capitalize()
        if col_name not in data and t in mapping:
            if t == 'empresa' and company_name:
                data[col_name] = [company_name for _ in range(rows)]
            else:
                data[col_name] = [mapping[t]() for _ in range(rows)]
    
    # 5. Cálculo do Total (se solicitado e houver dependências)
    if 'total' in types:
        # Garante que quantidade e valor existam
        qtds = data.get('Quantidade', [random.randint(1, 5) for _ in range(rows)])
        precos = data.get('Valor unitario', [round(random.uniform(50, 5000), 2) for _ in range(rows)])
        data['Quantidade'] = qtds
        data['Valor unitario'] = precos
        data['Total'] = [round(float(q) * float(v), 2) for q, v in zip(qtds, precos)]
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="Gerador de planilha de dados fictícios")
    parser.add_argument("-r", "--rows", type=int, default=10, help="Quantidade de linhas a gerar")
    parser.add_argument("-t", "--types", nargs="+", default=['nome', 'email', 'telefone'], help="Tipos de dados")
    parser.add_argument("-o", "--output", type=str, default="dados_ficticios.csv", help="Nome do arquivo de saída")
    parser.add_argument("-c", "--company", type=str, default=None, help="Nome da empresa")
    
    args = parser.parse_args()
    df = generate_data(args.rows, args.types, company_name=args.company)
    
    if args.output.endswith('.xlsx'): df.to_excel(args.output, index=False)
    elif args.output.endswith('.json'): df.to_json(args.output, orient='records', indent=4, force_ascii=False)
    else: df.to_csv(args.output, index=False, encoding='utf-8-sig', decimal=',')
    print(f"Arquivo '{args.output}' gerado com sucesso!")

if __name__ == "__main__":
    main()
