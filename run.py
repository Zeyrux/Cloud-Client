from app import Client
from werkzeug.security import generate_password_hash
import json

print(generate_password_hash(json.load(open("data.json", "r"))["password"]))
Client().start()
