import sys
from PyQt5 import QtWidgets, uic
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

class ClientApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("client.ui", self)
        self.connectButton.clicked.connect(self.derive_shared_secret)
        self.private_key = None  # Lưu private key client

    def log(self, message):
        self.logTextEdit.append(message)

    def derive_shared_secret(self):
        try:
            self.log("Đang tải khóa công khai của server...")
            with open("server_public_key.pem", "rb") as f:
                server_public_key = serialization.load_pem_public_key(f.read())

            parameters = server_public_key.parameters()
            self.private_key = parameters.generate_private_key()
            public_key = self.private_key.public_key()

            # Lưu public key client ra file để server đọc
            client_public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open("client_public_key.pem", "wb") as f:
                f.write(client_public_pem)

            shared_secret = self.private_key.exchange(server_public_key)
            self.log("Shared Secret (Client):\n" + shared_secret.hex())
        except Exception as e:
            self.log(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
