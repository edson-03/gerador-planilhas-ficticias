import streamlit as st
import pandas as pd
from generator import generate_data
import io

st.set_page_config(page_title="Gerador de Dados Fictícios", page_icon="📊", layout="wide")

st.title("📊 Gerador de Planilha de Dados Fictícios")
st.markdown("""
Crie planilhas personalizadas com dados aleatórios para testes, apresentações ou estudos.
""")

with st.sidebar:
    st.header("Configurações")
    rows = st.number_input("Quantidade de linhas", min_value=1, max_value=10000, value=100)
    
    st.subheader("Campos Disponíveis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Pessoais**")
        nome = st.checkbox("Nome", value=True)
        email = st.checkbox("Email", value=True)
        cpf = st.checkbox("CPF")
        telefone = st.checkbox("Telefone")
        profissao = st.checkbox("Profissão")
        
    with col2:
        st.write("**Localização**")
        endereco = st.checkbox("Endereço")
        cidade = st.checkbox("Cidade")
        estado = st.checkbox("Estado")
        cep = st.checkbox("CEP")
        empresa = st.checkbox("Empresa")

    st.write("---")
    st.write("**Vendas e Tempo**")
    vendas_mode = st.checkbox("Incluir Dados de Vendas", value=False)
    
    if vendas_mode:
        data_venda = st.checkbox("Data da Venda", value=True)
        produto = st.checkbox("Produto", value=True)
        categoria = st.checkbox("Categoria", value=True)
        quantidade = st.checkbox("Quantidade", value=True)
        valor_unitario = st.checkbox("Valor Unitário", value=True)
    else:
        data_venda = False
        produto = False
        categoria = False
        quantidade = False
        valor_unitario = False

# Mapeamento dos checkboxes para as chaves do generator
selected_types = []
if nome: selected_types.append('nome')
if email: selected_types.append('email')
if cpf: selected_types.append('cpf')
if telefone: selected_types.append('telefone')
if profissao: selected_types.append('profissao')
if endereco: selected_types.append('endereco')
if cidade: selected_types.append('cidade')
if estado: selected_types.append('estado')
if cep: selected_types.append('cep')
if empresa: selected_types.append('empresa')

if vendas_mode:
    if data_venda: selected_types.append('data')
    if produto: selected_types.append('produto')
    if categoria: selected_types.append('categoria')
    if quantidade: selected_types.append('quantidade')
    if valor_unitario: selected_types.append('valor_unitario')

if st.button("🚀 Gerar Dados", type="primary"):
    if not selected_types:
        st.warning("Por favor, selecione pelo menos um campo para gerar os dados.")
    else:
        with st.spinner("Gerando dados..."):
            df = generate_data(rows, selected_types)
            
            st.success(f"✅ {rows} linhas geradas com sucesso!")
            
            # Mostrar preview
            st.subheader("Preview dos Dados")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Opções de Download
            st.write("---")
            st.subheader("📥 Baixar Planilha")
            
            c_csv, c_xlsx = st.columns(2)
            
            with c_csv:
                # CSV formatado para Excel (ponto e vírgula e vírgula decimal)
                csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',').encode('utf-8-sig')
                st.download_button(
                    label="Baixar em CSV (Excel)",
                    data=csv,
                    file_name="dados_gerados.csv",
                    mime="text/csv",
                )
            
            with c_xlsx:
                # Formato Excel nativo
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Dados')
                xlsx_data = output.getvalue()
                st.download_button(
                    label="Baixar em XLSX (Excel Nativo)",
                    data=xlsx_data,
                    file_name="dados_gerados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            
            # Mini Dashboard se for vendas
            if vendas_mode and 'Total' in df.columns:
                st.write("---")
                st.subheader("Resumo das Vendas Geradas")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total de Vendas", f"R$ {df['Total'].sum():,.2f}")
                c2.metric("Qtd Total Itens", f"{df['Quantidade'].sum()}")
                c3.metric("Ticket Médio", f"R$ {df['Total'].mean():,.2f}")
                
                if 'Categoria' in df.columns:
                    st.bar_chart(df.groupby('Categoria')['Total'].sum())

else:
    st.info("Selecione as opções na barra lateral e clique em 'Gerar Dados' para começar.")
