import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout

class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PFM Converter")

         # Obtém tamanho da tela
        screen = QApplication.primaryScreen().geometry()
        largura_tela = screen.width()
        altura_tela = screen.height()

        # Define tamanho = 30%
        self.resize(int(largura_tela * 0.30), int(altura_tela * 0.30))

        layout = QVBoxLayout()

        self.btn_selecionar = QPushButton("Selecionar arquivo")
        self.btn_selecionar.clicked.connect(self.selecionar_arquivo)

        layout.addWidget(self.btn_selecionar)
        self.setLayout(layout)

    def selecionar_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Escolher arquivo")
        if caminho:
            print("Arquivo selecionado:", caminho)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec())
