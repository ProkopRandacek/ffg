from http.server import BaseHTTPRequestHandler, HTTPServer
from main import GenBP
from recipe import recipes
import time

hostName = "localhost"
serverPort = 35715


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        print("REQUEST: ", self.path)
        if ":" not in self.path:
            print(": not in path")
            self.send_response(400)
            self.end_headers()
            return
        item, amount = self.path[1:].split(":")
        if item not in recipes.keys():
            print(f"{item} not in recipes")
            self.send_response(400)
            self.end_headers()
            return
        try:
            amount = float(amount)
        except ValueError:
            print("second value is not float")
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("\n".join(GenBP(item, amount)), "utf-8"))


if __name__ == "__main__":
    server = HTTPServer((hostName, serverPort), Server)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")
