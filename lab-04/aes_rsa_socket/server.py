# from Crypto.Cipher import AES, PKCS1_OAEP 
# from Crypto.PublicKey import RSA 
# from Crypto.Random import get_random_bytes 
# from Crypto.Util.Padding import pad, unpad 
# import socket 
# import threading 

# # Initialize server socket 
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# server_socket.bind(('localhost', 12345)) 
# server_socket.listen(5) 
# print("Server đang lắng nghe cổng 12345...")

# # Generate RSA key pair 
# server_key = RSA.generate(2048) 

# # List of connected clients 
# clients = [] 

# # Function to encrypt message 
# def encrypt_message(key, message): 
#     cipher = AES.new(key, AES.MODE_CBC) 
#     ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size)) 
#     return cipher.iv + ciphertext 

# # Function to decrypt message 
# def decrypt_message(key, encrypted_message): 
#     iv = encrypted_message[:AES.block_size] 
#     ciphertext = encrypted_message[AES.block_size:] 
#     cipher = AES.new(key, AES.MODE_CBC, iv) 
#     decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size) 
#     return decrypted_message.decode()

# # Function to handle client connection 
# def handle_client(client_socket, client_address): 
#     print(f"Connected with {client_address}") 
#     # Send server's public key to client 
#     client_socket.send(server_key.publickey().export_key(format='PEM')) 
#     # Receive client's public key 
#     client_received_key = RSA.import_key(client_socket.recv(2048))
#     # Generate AES key for message encryption 
#     aes_key = get_random_bytes(16) 
#     # Encrypt the AES key using the client's public key 
#     cipher_rsa = PKCS1_OAEP.new(client_received_key) 
#     encrypted_aes_key = cipher_rsa.encrypt(aes_key) 
#     client_socket.send(encrypted_aes_key) 
#     # Add client to the list 
#     clients.append((client_socket, aes_key)) 
#     while True: 
#         encrypted_message = client_socket.recv(1024) 
#         if not encrypted_message:
#             break
#         decrypted_message = decrypt_message(aes_key, encrypted_message) 
#         print(f"Received from {client_address}: {decrypted_message}") 
        
#         # Send received message to all other clients 
#         for client, key in clients: 
#             if client != client_socket: 
#                 encrypted = encrypt_message(key, decrypted_message) 
#                 client.send(encrypted)
        
#         if decrypted_message == "exit": 
#             break 
    
#     clients.remove((client_socket, aes_key)) 
#     client_socket.close() 
#     print(f"Connection with {client_address} closed") 

# # Accept and handle client connections 
# while True: 
#     print("Đang chờ client kết nối...") 
#     client_socket, client_address = server_socket.accept() 
#     client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) 
#     client_thread.start()

import sys
import socket
import threading
from PyQt5 import QtWidgets, uic
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ServerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ServerApp, self).__init__()
        uic.loadUi('server.ui', self)

        self.startButton.clicked.connect(self.start_server)
        self.stopButton.clicked.connect(self.stop_server)
        self.stopButton.setEnabled(False)

        self.server_socket = None
        self.clients = []  # Danh sách (socket, aes_key, address)
        self.server_key = RSA.generate(2048)
        self.running = False

    def log(self, message):
        self.logTextEdit.append(message)

    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ct = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ct

    def decrypt_message(self, key, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ct = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()

    def handle_client(self, client_socket, client_address):
        self.log(f"Client {client_address} connected.")
        # Gửi public key server
        client_socket.send(self.server_key.publickey().export_key(format='PEM'))

        # Nhận public key client
        client_pub_key_data = client_socket.recv(2048)
        client_pub_key = RSA.import_key(client_pub_key_data)

        # Tạo AES key mới
        aes_key = get_random_bytes(16)

        # Mã hóa AES key với public key client
        cipher_rsa = PKCS1_OAEP.new(client_pub_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        self.clients.append((client_socket, aes_key, client_address))
        self.update_client_list()

        try:
            while self.running:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                message = self.decrypt_message(aes_key, encrypted_message)
                self.log(f"{client_address}: {message}")

                # Gửi lại cho các client khác
                for c, key, addr in self.clients:
                    if c != client_socket:
                        try:
                            c.send(self.encrypt_message(key, message))
                        except Exception as e:
                            self.log(f"Send error to {addr}: {e}")

                if message.lower() == "exit":
                    break
        except Exception as e:
            self.log(f"Error with client {client_address}: {e}")

        self.clients.remove((client_socket, aes_key, client_address))
        client_socket.close()
        self.update_client_list()
        self.log(f"Client {client_address} disconnected.")

    def update_client_list(self):
        self.clientsList.clear()
        for _, _, addr in self.clients:
            self.clientsList.addItem(str(addr))

    def start_server(self):
        if self.running:
            return
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        self.running = True
        self.log("Server started and listening on port 12345")
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

        def accept_clients():
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
                except Exception as e:
                    if self.running:
                        self.log(f"Accept error: {e}")
                    break

        threading.Thread(target=accept_clients, daemon=True).start()

    def stop_server(self):
        if not self.running:
            return
        self.running = False
        self.server_socket.close()
        self.log("Server stopped.")
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        # Đóng các kết nối client
        for c, _, _ in self.clients:
            try:
                c.close()
            except:
                pass
        self.clients.clear()
        self.update_client_list()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    server_window = ServerApp()
    server_window.show()
    sys.exit(app.exec_())
