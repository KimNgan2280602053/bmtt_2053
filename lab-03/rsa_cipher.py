import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa_cipher import Ui_RSA_Cipher
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RSA_Cipher()
        self.ui.setupUi(self)
        self.ui.btn_generate_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5050/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5050/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5050/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_sign(self):
        url = "http://127.0.0.1:5050/api/rsa/sign"
        payload = {
            "message": self.ui.txt_information.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_signature.setPlainText(data["signature"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:", e)


    def call_api_verify(self):
        message = self.ui.txt_information.toPlainText().strip()
        signature = self.ui.txt_signature.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "Warning", "Please enter the message to verify.")
            return

        if not signature:
            QMessageBox.warning(self, "Warning", "Please enter the signature to verify.")
            return

        url = "http://127.0.0.1:5050/api/rsa/verify"
        payload = {
            "message": message,
            "signature": signature
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    QMessageBox.information(self, "Success", "Verified Successfully")
                else:
                    QMessageBox.information(self, "Failure", "Verification Failed")
            else:
                print(f"Error while calling API, status code: {response.status_code}")
                print("Response content:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())