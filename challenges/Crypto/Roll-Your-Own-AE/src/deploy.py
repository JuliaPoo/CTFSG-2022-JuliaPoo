from waitress import serve
from app import app
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5555

print("Deploying at %s:%d" % (HOST, PORT))
serve(app, host=HOST, port=PORT)
