import sys
from PyQt5 import QtWidgets, uic
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

class ServerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("server.ui", self)

        # Kết nối nút Start với hàm generate_key
        self.startButton.clicked.connect(self.generate_key)
        # Kết nối nút Calculate Shared Secret với hàm tính shared secret
        self.sharedButton.clicked.connect(self.calculate_shared_secret)

        self.private_key = None  # lưu private_key sau khi tạo

    def log(self, message):
        self.logTextEdit.append(message)

    def generate_key(self):
        self.log("Đang tạo khóa Diffie-Hellman...")
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        self.private_key = parameters.generate_private_key()
        public_key = self.private_key.public_key()

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("server_public_key.pem", "wb") as f:
            f.write(pem)

        self.log("Đã lưu khóa công khai server vào 'server_public_key.pem'.")

    def calculate_shared_secret(self):
        if self.private_key is None:
            self.log("Vui lòng tạo khóa trước bằng nút Start.")
            return

        try:
            self.log("Đang tải khóa công khai của client từ 'client_public_key.pem'...")
            with open("client_public_key.pem", "rb") as f:
                client_public_key = serialization.load_pem_public_key(f.read())

            # Tính shared secret
            shared_secret = self.private_key.exchange(client_public_key)
            self.log("Shared Secret tính được:\n" + shared_secret.hex())

        except Exception as e:
            self.log(f"Lỗi khi tính shared secret: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())
