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

def collect_player_data(message):
    data = json.loads(message.get("Data"))
    player = data.get("Players", [])
    player = player[0]
    
    if "Boost" in player:
        with open("data.txt", "a", encoding="utf-8") as data:
            data.write(f"{player["Boost"]}, ")

    with open("data.txt", "a", encoding="utf-8") as data:
        data.write("\n")


#game = data.get("Game")

def main():
    last_message = client.get_message()

    if last_message["Event"] == "UpdateState":
        collect_player_data(last_message)


if __name__ == "__main__":
    while True:
        main()
