import streamlit as st
import pandas as pd
from generator import generate_data
import io
from datetime import datetime, date

st.set_page_config(page_title="Gerador Pro", page_icon="📊", layout="wide")

# Custom CSS para melhorar a interface
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .css-1r6slb0 {
        padding: 2rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Gerador de Dados Fictícios Pro")
st.info("Configure as opções na barra lateral e utilize as abas para organizar seus campos.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações Gerais")
    rows = st.number_input("Quantidade de linhas", min_value=1, max_value=50000, value=100)
    
    st.write("---")
    st.subheader("🏢 Personalização")
    empresa_check = st.checkbox("Incluir Empresa")
    company_name_input = None
    if empresa_check:
        company_name_input = st.text_input("Nome da Empresa", placeholder="Deixe em branco para aleatório")
    
    st.write("---")
    st.subheader("📅 Período de Datas")
    hoje = date.today()
    ano_passado = hoje.replace(year=hoje.year - 1)
    data_inicio, data_fim = st.date_input(
        "Intervalo",
        value=(ano_passado, hoje),
        max_value=hoje
    )

# --- CORPO PRINCIPAL (ABAS) ---
tab1, tab2, tab3, tab4 = st.tabs(["👤 Pessoais & Documentos", "📍 Localização", "🕒 Tempo", "💰 Vendas"])

selected_types = []

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 Básicos")
        if st.checkbox("Nome", value=True): selected_types.append('nome')
        if st.checkbox("Email", value=True): selected_types.append('email')
        if st.checkbox("Telefone"): selected_types.append('telefone')
        if st.checkbox("Profissão"): selected_types.append('profissao')
        if empresa_check: selected_types.append('empresa')
    with col2:
        st.markdown("### 🆔 Documentos")
        if st.checkbox("CPF"): selected_types.append('cpf')
        if st.checkbox("RG"): selected_types.append('rg')
        if st.checkbox("CNPJ"): selected_types.append('cnpj')

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🗺️ Endereço")
        if st.checkbox("Endereço Completo"): selected_types.append('endereco')
        if st.checkbox("CEP"): selected_types.append('cep')
    with col2:
        st.markdown("### 🏘️ Regional")
        if st.checkbox("Estado (Consistente)"): selected_types.append('estado')
        if st.checkbox("Cidade (Consistente)"): selected_types.append('cidade')

with tab3:
    st.markdown("### 🕒 Detalhes Temporais")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.checkbox("Data Completa"): selected_types.append('data')
        if st.checkbox("Dia"): selected_types.append('dia')
    with c2:
        if st.checkbox("Mês (Nº)"): selected_types.append('mes')
        if st.checkbox("Nome do Mês"): selected_types.append('nome_mes')
    with c3:
        if st.checkbox("Ano"): selected_types.append('ano')
        if st.checkbox("Semana do Ano"): selected_types.append('semana')

with tab4:
    st.markdown("### 💰 Itens e Valores")
    c1, c2 = st.columns(2)
    with c1:
        if st.checkbox("Produto (Preço Inteligente)"): selected_types.append('produto')
        if st.checkbox("Categoria"): selected_types.append('categoria')
        if st.checkbox("SKU"): selected_types.append('sku')
        if st.checkbox("ID do Pedido"): selected_types.append('id_pedido')
    with c2:
        if st.checkbox("Quantidade"): selected_types.append('quantidade')
        if st.checkbox("Valor Unitário"): selected_types.append('valor_unitario')
        if st.checkbox("Total (Calculado)"): selected_types.append('total')
        if st.checkbox("Status da Venda"): selected_types.append('status')
        if st.checkbox("Vendedor"): selected_types.append('vendedor')

st.write("---")

# --- BOTÃO DE GERAÇÃO ---
if st.button("🚀 GERAR PLANILHA", type="primary"):
    if not selected_types:
        st.warning("Selecione pelo menos um campo nas abas acima.")
    else:
        with st.spinner("Processando dados de alta qualidade..."):
            df = generate_data(rows, selected_types, 
                               start_date=data_inicio, 
                               end_date=data_fim,
                               company_name=company_name_input if empresa_check else None)
            
            st.success(f"✅ {rows} linhas geradas com sucesso!")
            
            # Preview
            st.subheader("📋 Preview (Top 10)")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Downloads
            st.write("---")
            st.subheader("📥 Exportar Arquivo")
            down_col1, down_col2, down_col3 = st.columns(3)
            
            with down_col1:
                csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',').encode('utf-8-sig')
                st.download_button("Baixar CSV (Excel)", csv, "dados.csv", "text/csv")
            
            with down_col2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Dados')
                st.download_button("Baixar XLSX (Nativo)", output.getvalue(), "dados.xlsx", "application/vnd.ms-excel")
                
            with down_col3:
                json_data = df.to_json(orient='records', indent=4, force_ascii=False).encode('utf-8')
                st.download_button("Baixar JSON", json_data, "dados.json", "application/json")
            
            # Dashboards
            if any(f in df.columns for f in ['Total', 'Categoria', 'Status', 'Vendedor']):
                st.write("---")
                st.subheader("📈 Análise Rápida")
                
                m1, m2, m3 = st.columns(3)
                if 'Total' in df.columns:
                    m1.metric("Faturamento", f"R$ {df['Total'].sum():,.2f}")
                    m2.metric("Ticket Médio", f"R$ {df['Total'].mean():,.2f}")
                if 'Quantidade' in df.columns:
                    m3.metric("Itens Vendidos", int(df['Quantidade'].sum()))
                
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    if 'Categoria' in df.columns and 'Total' in df.columns:
                        st.write("**Faturamento por Categoria**")
                        st.bar_chart(df.groupby('Categoria')['Total'].sum())
                    elif 'Status' in df.columns:
                        st.write("**Distribuição por Status**")
                        st.bar_chart(df['Status'].value_counts())
                
                with chart_col2:
                    if 'Data' in df.columns and 'Total' in df.columns:
                        st.write("**Evolução Diária**")
                        df_time = df.groupby('Data')['Total'].sum().reset_index().sort_values('Data')
                        st.line_chart(df_time.set_index('Data'))
                    elif 'Vendedor' in df.columns:
                        st.write("**Ranking Vendedores**")
                        st.bar_chart(df['Vendedor'].value_counts())
