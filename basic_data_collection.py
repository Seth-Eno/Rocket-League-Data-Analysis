from client import GameClient
import json
import time

# Sometimes the data arrives as a JSON string instead of a dictionary:
#
# if isinstance(data, str):
#     data = json.loads(data)

# welp i just realized player position isnt included...
# ig lets try
# Update state 
#   player: Touches, bHasCar, Speed, Boost, bBoosting, bOnGround, bOnWall, bPowersliding, bSupersonic, 
#   ball: Speed, TeamNum
# ball hit
# Name, PreHitSpeed, PostHitSpeed, X, Y, Z

client = GameClient()
client.connect()

def print_boost(message):
    data = json.loads(message.get("Data"))

    players = data.get("Players", [])
    game = data.get("Game")
    for i in range(len(players)):
        if ("Boost" in players[i]) and ("TimeSeconds" in game):
            print(f"[{game["TimeSeconds"]}] {players[i]["Name"]}: {players[i]["Boost"]}")


def main():
    last_message = client.get_message()

    if last_message["Event"] == "UpdateState":
        print_boost(last_message)




if __name__ == "__main__":
    while True:
        main()
