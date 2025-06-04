from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import serialization

class DigitalSignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/digital_signature.ui", self)
        self.setWindowTitle("Chữ ký số RSA + ECC")

        # Kết nối nút
        self.generateRsaButton.clicked.connect(self.generate_rsa_signature)
        self.verifyRsaButton.clicked.connect(self.verify_rsa_signature)
        self.generateEccButton.clicked.connect(self.generate_ecc_signature)
        self.verifyEccButton.clicked.connect(self.verify_ecc_signature)

        # Tạo khóa sẵn
        self.rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.ecc_private_key = ec.generate_private_key(ec.SECP256R1())

    def generate_rsa_signature(self):
        text = self.inputTextEdit.toPlainText().encode()
        signature = self.rsa_private_key.sign(
            text,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.rsaSignatureEdit.setPlainText(signature.hex())

    def verify_rsa_signature(self):
        try:
            text = self.inputTextEdit.toPlainText().encode()
            signature = bytes.fromhex(self.rsaSignatureEdit.toPlainText())
            self.rsa_private_key.public_key().verify(
                signature,
                text,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.rsaStatusLabel.setText("✅ Hợp lệ")
        except Exception:
            self.rsaStatusLabel.setText("❌ Không hợp lệ")

    def generate_ecc_signature(self):
        text = self.inputTextEdit.toPlainText().encode()
        signature = self.ecc_private_key.sign(text, ec.ECDSA(hashes.SHA256()))
        self.eccSignatureEdit.setPlainText(signature.hex())

    def verify_ecc_signature(self):
        try:
            text = self.inputTextEdit.toPlainText().encode()
            signature = bytes.fromhex(self.eccSignatureEdit.toPlainText())
            self.ecc_private_key.public_key().verify(signature, text, ec.ECDSA(hashes.SHA256()))
            self.eccStatusLabel.setText("✅ Hợp lệ")
        except Exception:
            self.eccStatusLabel.setText("❌ Không hợp lệ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalSignatureApp()
    window.show()
    sys.exit(app.exec_())
