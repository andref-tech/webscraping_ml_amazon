import bd
import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QListWidget, QTableView,QProgressBar
)
from PySide6.QtCore import Qt, QAbstractTableModel
import backend

def open_main_window(self):
    """Função global para abrir a janela principal."""
    self.main_window = MainWindow()  # Cria uma instância da tela principal
    self.main_window.show()  # Exibe a tela principal
    self.close()  # Fecha a janela atual


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Tela Principal")  # Define o título da janela

        # Configuração do layout
        layout = QVBoxLayout()

        # Botão para realizar nova pesquisa
        self.new_search_button = QPushButton("Realizar nova pesquisa")
        self.new_search_button.setStyleSheet("background-color: #8e2dc5; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.new_search_button.clicked.connect(self.open_search_window)  # Conecta o botão à função
        layout.addWidget(self.new_search_button)  # Adiciona o botão ao layout

        # Botão para visualizar pesquisas
        self.view_searches_button = QPushButton("Visualizar pesquisas")
        self.view_searches_button.setStyleSheet("background-color: #8e2dc5; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.view_searches_button.clicked.connect(self.open_view_searches_window)  # Conecta o botão à função
        layout.addWidget(self.view_searches_button)  # Adiciona o botão ao layout

        # Widget central
        container = QWidget()
        container.setLayout(layout)  # Define o layout para o container
        self.setCentralWidget(container)  # Define o widget central da janela

    def open_search_window(self):
        """Abre a janela de pesquisa de produtos."""
        self.search_window = SearchWindow()
        self.search_window.show()
        self.close()

    def open_view_searches_window(self):
        """Abre a janela para visualizar as pesquisas."""
        self.view_searches_window = ViewSearchesWindow()  # Corrigido para passar dados se necessário
        self.view_searches_window.show()
        self.close()


class SearchWindow(QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setWindowTitle("Buscar Produto")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.product_label = QLabel("Digite o nome do produto:")
        layout.addWidget(self.product_label)

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Insira o nome do produto")
        layout.addWidget(self.product_input)

        self.search_button = QPushButton("Realizar busca")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def perform_search(self):
        product_name = self.product_input.text()
        # Aqui você pode adicionar a lógica de busca no banco de dados
        QMessageBox.information(self, "Busca Realizada", f"Buscando por: {product_name}")
        backend.busca(product_name)

    def closeEvent(self, event):
        """Reabre a MainWindow ao fechar esta janela."""
        open_main_window(self)


class ViewSearchesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Widgets Demo")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        # Label
        layout.addWidget(QLabel("Escolha o produto:"))

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.addItems(bd.get_table_names())  # Certifique-se de que isso retorna os nomes corretos
        layout.addWidget(self.list_widget)

        # Button
        button = QPushButton("Pesquisar")
        button.clicked.connect(self.open_pandas)
        layout.addWidget(button)

        # Progress Bar
        progress_bar = QProgressBar()
        progress_bar.setValue(50)
        layout.addWidget(progress_bar)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_pandas(self):
        """Abre a janela para visualizar as pesquisas."""
        selected_item = self.list_widget.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um produto.")
            return

        # Obtém o nome da tabela selecionada
        table_name = selected_item.text()

        # Cria a segunda janela e passa o nome da tabela
        self.view_searches_window = TablesSearch(table_name)
        self.view_searches_window.show()  # Exibe a nova janela
        self.close()  # Fecha a janela atual


class TablesSearch(QMainWindow):
    def __init__(self, table_name):
        super(TablesSearch, self).__init__()
        self.setWindowTitle("Visualizador de Banco de Dados com Pandas e PySide6")
        self.setGeometry(100, 100, 600, 600)

        # Armazena o nome da tabela para uso posterior
        self.table_name = table_name

        # Configuração do layout
        layout = QVBoxLayout()

        # Botão para carregar dados
        self.load_button = QPushButton("Carregar Dados")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        # Tabela para exibir os dados
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # Widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        # Conecta ao banco de dados SQLite
        conn = bd.init_bd()
        cursor = conn.cursor()

        # Executa uma consulta SQL para selecionar todos os dados da tabela selecionada
        cursor.execute(f"SELECT * FROM {self.table_name.replace(' ', '_')}")  # Usa o nome da tabela armazenado

        # Carrega os dados no DataFrame do Pandas
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        # Fecha a conexão com o banco de dados
        conn.close()

        # Exibe os dados na tabela
        self.display_data(df)

    def display_data(self, df):
        model = PandasModel(df)
        self.table_view.setModel(model)

    def closeEvent(self, event):
        """Reabre a MainWindow ao fechar esta janela."""
        open_main_window(self)


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Configurações da janela
        self.setWindowTitle("Tela de Login")
        self.setGeometry(100, 100, 400, 200)

        # Estilo do layout
        layout = QVBoxLayout()

        # Campo de email
        self.email_label = QLabel("Email:")
        self.email_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email")
        self.email_input.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        layout.addWidget(self .email_input)

        # Campo de senha
        self.password_label = QLabel("Senha:")
        self.password_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Insira sua senha")
        self.password_input.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        layout.addWidget(self.password_input)

        # Botão de login
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #8e2dc5; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        # Widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # Aqui você pode adicionar lógica para verificar o email e a senha

        # Conecta ao banco de dados SQLite
        conn = bd.init_bd()
        cursor = conn.cursor()

        # Verifica se o nome de usuário e a senha estão na tabela de usuários
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, password))
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, "Login Bem-sucedido", "Bem-vindo!")
            open_main_window(self)
            '''self.main_window = MainWindow()  # Cria uma instância da tela principal
            self.main_window.show()  # Exibe a tela principal
            self.close()  # Fecha a janela atual'''
        else:
            QMessageBox.warning(self, "Login Falhou", "Nome de usuário ou senha incorretos.")

        conn.close()


# Configuração da aplicação Qt
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec_())