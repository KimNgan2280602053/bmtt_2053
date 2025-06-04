from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
from railfence_cipher import RailFenceCipher

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/railfence.ui", self)
        self.setWindowTitle("Rail Fence Cipher")

        # Gán biến rõ ràng để dễ debug
        self.text_input = self.findChild(type(self.plainTextEdit), "plainTextEdit")
        self.rail_input = self.findChild(type(self.railsSpinBox), "railsSpinBox")
        self.result_output = self.findChild(type(self.resultTextEdit), "resultTextEdit")

        self.encrypt_btn = self.findChild(type(self.encryptButton), "encryptButton")
        self.decrypt_btn = self.findChild(type(self.decryptButton), "decryptButton")

        # Kết nối nút
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        self.decrypt_btn.clicked.connect(self.decrypt_text)

        self.cipher = RailFenceCipher()

    def encrypt_text(self):
        try:
            text = self.text_input.toPlainText()
            rails = self.rail_input.value()
            if text and rails >= 2:
                result = self.cipher.rail_fence_encrypt(text, rails)
                self.result_output.setPlainText(result)
            else:
                self.result_output.setPlainText("Vui lòng nhập văn bản và số rail >= 2.")
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi mã hóa: {e}")

    def decrypt_text(self):
        try:
            text = self.text_input.toPlainText()
            rails = self.rail_input.value()
            if text and rails >= 2:
                result = self.cipher.rail_fence_decrypt(text, rails)
                self.result_output.setPlainText(result)
            else:
                self.result_output.setPlainText("Vui lòng nhập văn bản và số rail >= 2.")
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi giải mã: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())
