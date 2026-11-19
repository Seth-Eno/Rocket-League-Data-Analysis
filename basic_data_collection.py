from client import GameClient

client = GameClient()

def main():
    client.connect()
    print(client.get_messages())





if __name__ == "__main__":
    while True:
        main()
