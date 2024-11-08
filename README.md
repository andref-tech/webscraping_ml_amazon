# Webscraping de Valores - Mercado Livre e Amazon <img src= 'https://github.com/andref-tech/andref-tech/blob/main/Python-programming-logo-on-transparent-background-PNG.png' width='70'>
# Descrição do Projeto 

Este projeto é uma aplicação desktop desenvolvida em Python utilizando a biblioteca **PySide6** para a interface gráfica e **SQLite** para o gerenciamento de banco de dados. A aplicação permite ao usuário realizar buscas de produtos em sites como **Mercado Livre e Amazon**, visualizar os resultados e armazenar as informações em um banco de dados.

## Estrutura do Projeto

O projeto é composto por três arquivos principais:

1. **app.py**: O arquivo principal que contém a lógica da interface gráfica e a interação do usuário.
2. **backend.py**: Este arquivo contém a lógica de busca de produtos utilizando Selenium, permitindo a extração de dados de sites de e-commerce.
3. **bd.py**: Este arquivo gerencia a conexão com o banco de dados SQLite, incluindo a criação de tabelas e a inserção de dados.

## Funcionalidades

- **Tela de Login**: Permite que os usuários façam login utilizando um email e senha.
- **Busca de Produtos**: Após o login, o usuário pode realizar buscas de produtos digitando o nome do produto desejado.
- **Visualização de Pesquisas**: O usuário pode visualizar as pesquisas realizadas e os produtos encontrados.
- **Armazenamento em Banco de Dados**: Os dados dos produtos encontrados são armazenados em um banco de dados SQLite.

## Requisitos

- Python 3.x
###### Bibliotecas Python (os mesmos estão no arquivo requirements.txt):
- PySide6
- Selenium
- Pandas
- SQLite

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/andref-tech/webscraping_ml_amazon
   cd webscraping_ml_amazon
Instale as dependências necessárias:

bash

Verify

Open In Editor
Edit
Copy code
pip install PySide6 selenium pandas
Certifique-se de ter o geckodriver instalado e disponível no PATH para o Selenium funcionar corretamente com o Firefox.

## Como Usar
Execute o arquivo app.py:

bash

Verify

Open In Editor
Edit
Copy code
python app.py
Na tela de login, insira o email e a senha (o email padrão é teste_teste@hotmail.com e a senha é senha123).

Após o login, você terá acesso à tela principal, onde poderá realizar novas pesquisas ou visualizar pesquisas anteriores.

Ao realizar uma busca, os produtos encontrados serão exibidos e armazenados no banco de dados.

###### Estrutura do Banco de Dados
O banco de dados SQLite criado contém as seguintes tabelas:

**usuarios**: Contém informações dos usuários que podem fazer login.
<nome_do_produto>: Tabelas dinâmicas criadas para cada produto pesquisado, contendo as colunas:
**id: **Identificador único do registro.
**site:** Nome do site onde o produto foi encontrado.
**nome:** Nome do produto.
**valor:** Preço do produto.
**link:** URL do produto.

### Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou um pull request.
