# from Crypto.Cipher import AES, PKCS1_OAEP 
# from Crypto.PublicKey import RSA 
# from Crypto.Random import get_random_bytes 
# from Crypto.Util.Padding import pad, unpad 
# import socket 
# import threading 
# import hashlib
# # Initialize client socket 
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# client_socket.connect(('localhost', 12345)) 
# # Generate RSA key pair 
# client_key = RSA.generate (2048) 
# # Receive server's public key 
# server_public_key = RSA.import_key(client_socket.recv(2048)) 
# # Send client's public key to the server 
# client_socket.send(client_key.publickey().export_key(format='PEM')) 
# # Receive encrypted AES key from the server 
# encrypted_aes_key = client_socket.recv(2048) 
# # Decrypt the AES key using client's private key 
# cipher_rsa = PKCS1_OAEP.new(client_key) 
# aes_key = cipher_rsa.decrypt(encrypted_aes_key)
# #Function to encrypt message 
# def encrypt_message(key, message): 
#     cipher = AES.new(key, AES.MODE_CBC) 
#     ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size)) 
#     return cipher.iv + ciphertext 
# #Function to decrypt message 
# def decrypt_message(key, encrypted_message): 
#     iv = encrypted_message[:AES.block_size] 
#     ciphertext = encrypted_message[AES.block_size:] 
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     decrypted_message = unpad(cipher.decrypt (ciphertext), AES.block_size) 
#     return decrypted_message.decode() 
# # Function to receive messages from server 
# def receive_messages(): 
#     while True: 
#         encrypted_message = client_socket.recv(1024) 
#         decrypted_message = decrypt_message(aes_key, encrypted_message) 
#         print("Received:", decrypted_message)
# # Start the receiving thread 
# receive_thread = threading.Thread(target=receive_messages) 
# receive_thread.start() 
# # Send messages from the client 
# while True: 
#     message = input("Enter message ('exit' to quit): ") 
#     encrypted_message = encrypt_message(aes_key, message) 
#     client_socket.send(encrypted_message) 
#     if message == "exit": 
#         break 
# # Close the connection when done 
# client_socket.close()

import sys
import socket
import threading
from PyQt5 import QtWidgets, uic
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ClientApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClientApp, self).__init__()
        uic.loadUi('client.ui', self)

        self.sendButton.clicked.connect(self.send_message)

        self.client_socket = None
        self.aes_key = None
        self.server_public_key = None
        self.client_key = RSA.generate(2048)

        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', 12345))
            self.log_message("Connected to server")

            # Nhận public key server
            server_pub_key_data = self.client_socket.recv(2048)
            self.server_public_key = RSA.import_key(server_pub_key_data)

            # Gửi public key client
            self.client_socket.send(self.client_key.publickey().export_key(format='PEM'))

            # Nhận AES key đã mã hóa
            encrypted_aes_key = self.client_socket.recv(2048)

            # Giải mã AES key
            cipher_rsa = PKCS1_OAEP.new(self.client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

            # Bắt đầu luồng nhận tin nhắn
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.log_message(f"Không thể kết nối server: {e}")

    def encrypt_message(self, message):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ct_bytes

    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ct = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()

    def send_message(self):
        message = self.messageEdit.text()
        if message:
            try:
                encrypted = self.encrypt_message(message)
                self.client_socket.send(encrypted)
                self.chatBox.append(f"You: {message}")
                self.messageEdit.clear()
                if message.lower() == "exit":
                    self.client_socket.close()
                    self.close()
            except Exception as e:
                self.log_message(f"Send error: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = self.decrypt_message(data)
                self.chatBox.append(f"Server: {message}")
            except Exception as e:
                self.log_message(f"Receive error: {e}")
                break

    def log_message(self, msg):
        self.chatBox.append(msg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client_window = ClientApp()
    client_window.show()
    sys.exit(app.exec_())



