from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
from transposition_cipher import TranspositionCipher

class TranspositionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/transposition.ui", self)
        self.setWindowTitle("Transposition Cipher")

        self.encryptButton.clicked.connect(self.encrypt_text)
        self.decryptButton.clicked.connect(self.decrypt_text)

        self.cipher = TranspositionCipher()

    def encrypt_text(self):
        text = self.plainTextEdit.toPlainText()
        key = self.keySpinBox.value()
        if text and key:
            result = self.cipher.encrypt(text, key)
            self.resultTextEdit.setPlainText(result)

    def decrypt_text(self):
        text = self.plainTextEdit.toPlainText()
        key = self.keySpinBox.value()
        if text and key:
            result = self.cipher.decrypt(text, key)
            self.resultTextEdit.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranspositionApp()
    window.show()
    sys.exit(app.exec_())
