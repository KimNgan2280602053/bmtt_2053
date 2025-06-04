from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
from playfair_cipher import PlayFairCipher

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Loading UI...")
        uic.loadUi("ui/playfair.ui", self)
        self.setWindowTitle("Playfair Cipher")

        self.encryptButton.clicked.connect(self.encrypt_text)
        self.decryptButton.clicked.connect(self.decrypt_text)

        self.cipher = PlayFairCipher()
        print("UI loaded and connected.")

    def encrypt_text(self):
        print("Encrypt clicked")
        text = self.plainTextEdit.toPlainText()
        key = self.keyLineEdit.text()
        if text and key:
            matrix = self.cipher.create_playfair_matrix(key)
            result = self.cipher.playfair_encrypt(text, matrix)
            self.resultTextEdit.setPlainText(result)

    def decrypt_text(self):
        print("Decrypt clicked")
        text = self.plainTextEdit.toPlainText()
        key = self.keyLineEdit.text()
        if text and key:
            matrix = self.cipher.create_playfair_matrix(key)
            result = self.cipher.playfair_decrypt(text, matrix)
            self.resultTextEdit.setPlainText(result)

if __name__ == "__main__":
    print("App starting...")
    app = QApplication(sys.argv)
    window = PlayfairApp()
    print("Showing window...")
    window.show()
    sys.exit(app.exec_())
