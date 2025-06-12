from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class DebugWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 GET-запит на {self.path}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        print(f"\n📥 POST-запит на {self.path}")
        print("🔽 Headers:")
        for key, value in self.headers.items():
            print(f"  {key}: {value}")
        print("🔽 Body:")
        print(body.decode())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RECEIVED")

    def log_message(self, format, *args):
        return

def run():
    server_address = ('', 8070)
    httpd = HTTPServer(server_address, DebugWebhookHandler)
    print("🚀 Debug-сервер запущено на http://localhost:8070")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
