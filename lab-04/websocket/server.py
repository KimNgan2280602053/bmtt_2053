import tornado.ioloop
import tornado.web
import tornado.websocket
import random
import time

clients = set()
fruits = ["apple", "banana", "grape", "orange", "melon"]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket server is running!")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.add(self)
        print(f"Client connected, total clients: {len(clients)}")

    def on_close(self):
        clients.discard(self)
        print(f"Client disconnected, total clients: {len(clients)}")

    def check_origin(self, origin):
        return True  # Cho phép mọi origin

def send_fruit():
    if clients:
        fruit = random.choice(fruits)
        print(f"Sending message '{fruit}' to {len(clients)} client(s).")
        for client in clients:
            client.write_message(fruit)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket/", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on ws://localhost:8888/websocket/")
    
    # Gửi trái cây mỗi 2 giây
    tornado.ioloop.PeriodicCallback(send_fruit, 2000).start()
    tornado.ioloop.IOLoop.current().start()
