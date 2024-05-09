import http.server
import socketserver
import random
import string
import threading

class RandomURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><head><title>Test Server</title></head>")
        self.wfile.write(b"<body><h1>Welcome to the Test Server!</h1>")
        self.wfile.write(b"<p>This is a test server running on localhost with a random URL.</p>")
        self.wfile.write(b"<p>Requested URL: {}</p>".format(self.path.encode('utf-8')))
        self.wfile.write(b"</body></html>")

def start_test_server():
    # Generate a random URL
    random_url = ''.join(random.choices(string.ascii_lowercase, k=10))

    # Set up the server
    server_address = ('localhost', 8000)
    httpd = socketserver.TCPServer(server_address, RandomURLHandler)

    # Start the server in a new thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"Test server is running at http://localhost:8000/{random_url}")

if __name__ == "__main__":
    start_test_server()
