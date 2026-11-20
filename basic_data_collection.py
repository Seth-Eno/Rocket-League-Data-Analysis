from client import GameClient
import json
import time

# Sometimes the data arrives as a JSON string instead of a dictionary:
#
# if isinstance(data, str):
#     data = json.loads(data)

client = GameClient()
client.connect()

def print_boost(message):
    data = json.loads(message.get("Data"))

    players = data.get("Players", [])
    if "Boost" in players[0]:
        print(players[0]["Boost"])


def main():
    last_message = client.get_message()

    if last_message["Event"] == "UpdateState":
        print_boost(last_message)




if __name__ == "__main__":
    while True:
        main()
