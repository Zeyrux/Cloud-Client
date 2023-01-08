from socket import socket, AF_INET, SOCK_STREAM
from json import load
from pathlib import Path
from queue import Queue

from .models import Base
from .collect import Collector

from server_client_manager import send_authentication, send_file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_path: Path | str) -> None:
        self.path = db_path if type(db_path).__name__ == "Path" else Path(db_path)
        self.engine = create_engine(f"sqlite:///{self.path}", echo=True)
        self.Base = Base
        self.Base.metadata.create_all(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)()


class Client:
    def __init__(self) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        data = load(open("data.json", "r"))
        self.host = data["host"]
        self.port = data["port"]
        self.password = data["password"]
        self.queue = Queue()
        self.db = Database("db.db")
        self.collector = Collector(self.db.session)

    def run(self) -> None:
        self.collector.run()
        while True:
            self.queue.get()

    def sync(self) -> None:
        self.socket.connect((self.host, self.port))
        send_authentication(self.socket, self.password)
        print("Authenticated")
        send_file(self.socket, self.db.path, send_path=False, send_request_type=False)
