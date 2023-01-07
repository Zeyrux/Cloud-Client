import socket
from json import load

from server_client_manager import send_authentication


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = load(open("data.json", "r"))
        self.host = data["host"]
        self.port = data["port"]
        self.password = data["password"]

    def start(self) -> None:
        self.socket.connect((self.host, self.port))
        send_authentication(self.socket, self.password)
        print("Authenticated")
