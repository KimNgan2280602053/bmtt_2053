import socket
import ssl

# Thiết lập SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server-cert.crt", keyfile="server-key.key")

# Tạo socket TCP cơ bản
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('localhost', 12345))
    sock.listen(5)
    print("🟢 Server SSL đang lắng nghe tại cổng 12345...")

    # Bọc SSL cho socket
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            try:
                # Chấp nhận kết nối từ client
                client_conn, client_addr = ssock.accept()
                print(f"🔗 Đã kết nối từ {client_addr}")

                # Nhận dữ liệu từ client
                data = client_conn.recv(1024)
                if not data:
                    print("⚠️ Không nhận được dữ liệu.")
                    continue

                message = data.decode()
                print(f"📩 Tin nhắn nhận: {message}")

                # Phản hồi lại cho client
                response = f"Server đã nhận: {message}"
                client_conn.sendall(response.encode())

                client_conn.close()
                print("✅ Kết nối đã đóng.\n")

            except Exception as e:
                print(f"❌ Lỗi khi xử lý client: {e}")
