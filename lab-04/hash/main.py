import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import md5_hash
import md5_library
import sha_256
import sha_3
import blake2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('hash.ui', self)

        self.md5CustomButton.clicked.connect(self.handle_md5_custom)
        self.md5LibButton.clicked.connect(self.handle_md5_lib)
        self.sha256Button.clicked.connect(self.handle_sha256)
        self.sha3Button.clicked.connect(self.handle_sha3)
        self.blake2Button.clicked.connect(self.handle_blake2)

    def get_input_text(self):
        return self.inputLineEdit.text()

    def set_result_text(self, text):
        self.resultTextEdit.setPlainText(text)

    def handle_md5_custom(self):
        text = self.get_input_text()
        if not text:
            self.set_result_text("Vui lòng nhập chuỗi cần băm.")
            return
        hashed = md5_hash.md5(text.encode('utf-8'))
        self.set_result_text(hashed)

    def handle_md5_lib(self):
        text = self.get_input_text()
        if not text:
            self.set_result_text("Vui lòng nhập chuỗi cần băm.")
            return
        hashed = md5_library.calculate_md5(text)
        self.set_result_text(hashed)

    def handle_sha256(self):
        text = self.get_input_text()
        if not text:
            self.set_result_text("Vui lòng nhập chuỗi cần băm.")
            return
        hashed = sha_256.calculate_sha256_hash(text)
        self.set_result_text(hashed)

    def handle_sha3(self):
        text = self.get_input_text()
        if not text:
            self.set_result_text("Vui lòng nhập chuỗi cần băm.")
            return
        hashed_bytes = sha_3.sha3(text.encode('utf-8'))
        self.set_result_text(hashed_bytes.hex())

    def handle_blake2(self):
        text = self.get_input_text()
        if not text:
            self.set_result_text("Vui lòng nhập chuỗi cần băm.")
            return
        hashed_bytes = blake2.blake2(text.encode('utf-8'))
        self.set_result_text(hashed_bytes.hex())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
