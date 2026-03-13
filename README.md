# 📊 Gerador de Planilhas de Dados Fictícios

Este é um projeto em Python que permite gerar planilhas (CSV) com dados fictícios realistas. Ele inclui uma interface visual moderna feita com **Streamlit**, permitindo personalizar a quantidade de linhas e os tipos de dados (pessoais, localização e vendas).

## 🚀 Funcionalidades

- **Dados Pessoais**: Nome, Email, CPF, Telefone, Profissão, Empresa.
- **Localização**: Endereço, Cidade, Estado, CEP.
- **Módulo de Vendas**: Geração automática de produtos, categorias, quantidades, valores unitários e cálculo do valor total.
- **Módulo de Tempo**: Extração automática de Dia, Semana, Mês e Ano a partir da data da venda.
- **Interface Web**: Interface amigável para selecionar campos e baixar o arquivo.
- **Compatibilidade**: Exportação em CSV com codificação `utf-8-sig` (abre perfeitamente no Excel).

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/) - Manipulação de dados e exportação CSV.
- [Faker](https://faker.readthedocs.io/) - Geração de dados aleatórios realistas.
- [Streamlit](https://streamlit.io/) - Interface visual web.

## 📋 Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Você precisará instalar as dependências do projeto:

```bash
pip install -r requirements.txt
```

## 💻 Como Rodar

### Interface Visual (Recomendado)

Para iniciar a aplicação web:

```bash
python -m streamlit run app.py
```

Acesse no seu navegador através do endereço: `http://localhost:8501`

### Linha de Comando (Terminal)

Você também pode usar o script diretamente pelo terminal:

```bash
python generator.py -r 50 -t nome email cpf cidade -o meus_dados.csv
```

**Argumentos:**
- `-r`: Quantidade de linhas (padrão: 10).
- `-t`: Tipos de dados separados por espaço.
- `-o`: Nome do arquivo de saída.

## 📂 Estrutura do Projeto

- `app.py`: Interface visual com Streamlit.
- `generator.py`: Lógica principal de geração de dados.
- `requirements.txt`: Lista de dependências do projeto.
- `.gitignore`: Arquivos que não devem ser enviados para o repositório.

## 🤝 Contribuições

Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias!

---
Desenvolvido com ❤️ para facilitar a vida de desenvolvedores e analistas de dados.
