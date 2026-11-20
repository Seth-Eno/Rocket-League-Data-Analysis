import socket
import json
#import time

HOST = "127.0.0.1"
PORT = 49123

class GameClient:

    def connect(self):
        # connects to the game 
        self.decoder = json.JSONDecoder()
        self.buffer = ""  # leftover text that isn't a complete message yet
        self.sock = socket.create_connection((HOST, PORT))
        print("Connected!")
        return self


    def get_message(self):
        # reads messages, and passes each to handle_message.
        sock = self.sock
        decoder = self.decoder
        buffer = self.buffer
        chunk = sock.recv(65536)
        if chunk == b"":          # empty means the connection was closed
            sock.close
        buffer = buffer + chunk.decode()

        # The buffer may hold several messages, or only part of one
        while True:
            buffer = buffer.lstrip()   # remove leading whitespace
            if buffer == "":
                break
            try:
                message, end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                break                  # incomplete message, wait for more data
            buffer = buffer[end:]      # remove the message we just read
            return(message)
        sock.close()