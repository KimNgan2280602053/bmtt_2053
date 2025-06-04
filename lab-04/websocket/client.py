import sys
import asyncio
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import tornado.websocket
import tornado.platform.asyncio

class WebSocketClient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('websocket_client.ui', self)

        self.connectButton.clicked.connect(self.start_connection)
        self.connection = None

        # Tạo asyncio loop mới và cài đặt
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        tornado.platform.asyncio.AsyncIOMainLoop().install()

        # Dùng QTimer để chạy asyncio loop định kỳ (kết nối asyncio với PyQt5)
        self.asyncio_timer = QTimer()
        self.asyncio_timer.timeout.connect(self.run_loop_once)
        self.asyncio_timer.start(50)

    def run_loop_once(self):
        try:
            self.loop.call_soon(self.loop.stop)
            self.loop.run_forever()
        except Exception as e:
            print(f"Loop error: {e}")

    def start_connection(self):
        self.statusLabel.setText("Đang kết nối...")
        self.loop.create_task(self.connect_websocket())

    async def connect_websocket(self):
        try:
            self.connection = await tornado.websocket.websocket_connect("ws://localhost:8888/websocket/")
            self.statusLabel.setText("Đã kết nối")
            await self.read_message()
        except Exception as e:
            self.statusLabel.setText(f"Lỗi kết nối: {e}")

    async def read_message(self):
        while True:
            try:
                msg = await self.connection.read_message()
                if msg is None:
                    self.statusLabel.setText("Mất kết nối đến server.")
                    break
                self.append_message(msg)
            except Exception as e:
                self.statusLabel.setText(f"Lỗi khi nhận tin nhắn: {e}")
                break

    def append_message(self, message):
        current = self.messageTextEdit.toPlainText()
        self.messageTextEdit.setPlainText(current + message + "\n")

def main():
    app = QApplication(sys.argv)
    window = WebSocketClient()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
