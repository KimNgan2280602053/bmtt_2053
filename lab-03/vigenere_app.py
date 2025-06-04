from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
from vigenere_cipher import VigenereCipher

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Loading UI...")
        uic.loadUi("ui/vigenere.ui", self)
        self.setWindowTitle("Vigenère Cipher")

        self.encryptButton.clicked.connect(self.encrypt_text)
        self.decryptButton.clicked.connect(self.decrypt_text)

        self.cipher = VigenereCipher()
        print("UI loaded and buttons connected.")

    def encrypt_text(self):
        text = self.plainTextEdit.toPlainText()
        key = self.keyLineEdit.text()
        if text and key:
            result = self.cipher.encrypt_text(text, key)
            self.resultTextEdit.setPlainText(result)

    def decrypt_text(self):
        text = self.plainTextEdit.toPlainText()
        key = self.keyLineEdit.text()
        if text and key:
            result = self.cipher.decrypt_text(text, key)
            self.resultTextEdit.setPlainText(result)

if __name__ == "__main__":
    print("App starting...")
    app = QApplication(sys.argv)
    window = VigenereApp()
    print("Showing window...")
    window.show()
    sys.exit(app.exec_())
