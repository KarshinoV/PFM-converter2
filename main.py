import sys
import os
import subprocess
import scriptcontato
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon

class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icone.ico"))
        self.setWindowTitle("PFM Converter")

        # Obtém tamanho da tela
        screen = QApplication.primaryScreen().geometry()
        largura_tela = screen.width()
        altura_tela = screen.height()

        # Define tamanho = 30%
        self.resize(int(largura_tela * 0.30), int(altura_tela * 0.30))

        layout = QVBoxLayout()

        # Botão selecionar arquivo
        self.btn_selecionar = QPushButton("Selecionar arquivo")
        self.btn_selecionar.clicked.connect(self.selecionar_arquivo)
        layout.addWidget(self.btn_selecionar)

        # Botão abrir arquivo gerado (começa escondido)
        self.btn_abrir = QPushButton("Abrir arquivo gerado")
        self.btn_abrir.clicked.connect(self.abrir_arquivo)
        self.btn_abrir.setVisible(False)
        layout.addWidget(self.btn_abrir)

        self.caminho_gerado = None
        self.setLayout(layout)

    
    def selecionar_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Escolher arquivo")
        if not caminho:
            return

        print("Arquivo selecionado:", caminho)

        try:
            # inicia o processamento
            caminho_final = scriptcontato.iniciar(caminho)
            self.caminho_gerado = caminho_final

            # aplica delay de 1 segundo (1000 ms) antes de mostrar o botão
            QTimer.singleShot(1000, self.pos_processamento)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao processar arquivo:\n{e}")

    def pos_processamento(self):
        if not self.caminho_gerado or not os.path.exists(self.caminho_gerado):
            QMessageBox.critical(self, "Erro", "Arquivo gerado não encontrado.")
            return

        QMessageBox.information(self, "Sucesso", "Arquivo convertido com sucesso!")

        # mostra botão abrir arquivo
        self.btn_abrir.setVisible(True)


    def abrir_arquivo(self):
        if not self.caminho_gerado:
            return

        # Abrir conforme o sistema operacional
        if os.name == "nt":  # Windows
            os.startfile(self.caminho_gerado)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", self.caminho_gerado])
        else:  # Linux
            subprocess.call(["xdg-open", self.caminho_gerado])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec())
