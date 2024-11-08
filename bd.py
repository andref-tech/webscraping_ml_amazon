import site
import sqlite3
import os
import code

from matplotlib import table

# Obter o diretório atual onde o script .py está sendo executado
dir = os.path.dirname(os.path.abspath(__file__))

# Construir o caminho completo para o banco de dados
dir = os.path.join(dir, 'meu_banco_de_dados.db')


def init_bd():
# Verificar se o banco de dados já existe
    if os.path.exists(dir):
        conn = sqlite3.connect(dir)

    else:
        print("O banco de dados não existe. Será criado agora.")
        
        # Conectar ao banco de dados (ou criar se não existir)
        conn = sqlite3.connect(dir)

        # Criar um cursor
        cur = conn.cursor()

        # Criar uma tabela
        cur.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')

        # Inserir dados na tabela
        cur.execute('''
            INSERT INTO usuarios (nome, email, senha) VALUES
            ('admin', 'teste_teste@hotmail.com', 'senha123')
        ''')

        # Confirmar a transação
        conn.commit()

        print(f"Banco de dados criado em: {dir}")
        # Fechar a conexão
        conn.close()
    return conn

def verif_table(produto):
    print(f"Criar banco de dados {produto}")
    produto = produto.replace(" ", "_").upper()
    conn = init_bd()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(produto,))
    resultado = cur.fetchone()
    conn.close()
    if resultado:
        print(f"A tabela '{produto}' existe.")
        return True
    else:
        print(f"A tabela '{produto}' não existe.")
        return False


# Conectar ao banco de dados (ou criar se não existir)

def pesquisa(produto):
    print(f"Criar banco de dados {produto}")
    produto = produto.replace(" ", "_").upper()
    conn = init_bd()
    if conn is not None:
        cur = conn.cursor()
        table_exist = verif_table(produto)
        print(f"---------TAbela Existe? --- {table_exist}")
        if table_exist == False:
            cur.execute( f'''
                CREATE TABLE IF NOT EXISTS "{produto}" (
                    id INTEGER PRIMARY KEY,
                    site TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    valor REAL NOT NULL UNIQUE,
                    link TEXT NOT NULL
                )
            ''')
        else:
            while True:
                resp = input(f"A tabela {produto} já existe, gostaria de criar uma nova e sobrepor a antiga? S/N: ").upper()
                if resp =="S":
                    try:
                        # Comando para deletar a tabela
                        cur.execute(f"DROP TABLE IF EXISTS {produto}")
                        conn.commit()
                        print(f"Tabela '{produto}' deletada com sucesso.")
                        cur.execute( f'''
                            CREATE TABLE IF NOT EXISTS "{produto}" (
                                id INTEGER PRIMARY KEY,
                                site TEXT NOT NULL,
                                nome TEXT NOT NULL,
                                valor REAL NOT NULL,
                                link TEXT NOT NULL
                            )
                        ''')
                        break
                    except sqlite3.Error as e:
                        print(f"Erro ao deletar a tabela: {e}")
                elif resp =="N":
                    print(f"Processo de pesquisa de {produto} encerrado")
                    break
                else:
                    print("Resposta inscorreta. tente novamente.")



        conn.close
    else:
        print("Erro ao conectar ao DB")

def include_data(Site,produto,Nome,Preco,Link):
        produto = produto.replace(" ", "_").upper()
        conn = init_bd()
        cur = conn.cursor()
        if conn is not None:
            cur.execute(f'''INSERT INTO '{produto}' (site,nome, valor, link) VALUES ('{Site}','{Nome}', '{Preco}', '{Link}')''')
            # Confirmar a transação
            conn.commit()
        else:
            print("Erro ao se conectar ao servidor")

def get_table_names():
    """Retorna uma lista com os nomes das tabelas do banco de dados."""
    # Conecta ao banco de dados
    conn = init_bd()
    cursor = conn.cursor()

    # Executa a consulta para obter os nomes das tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'AND name !='usuarios';")
    tables = cursor.fetchall()  # Recupera todos os resultados

    # Fecha a conexão
    conn.close()

    # Extrai os nomes das tabelas da lista de tuplas
    table_names = [table[0].replace('_', ' ') for table in tables]
    print("lista")
    print(table_names)
    return table_names

# Obtém e imprime os nomes das tabelas
tables = get_table_names()
print("Tabelas no banco de dados:")
for table in tables:
    print(table)

#Abrir o terminal
#code.interact(local=locals())





