from client import GameClient
import json
import time
from pynput import keyboard
from pynput.keyboard import KeyCode

# keep the program running until Esc

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
message = client.get_message()

def get_name(message):
    data = json.loads(message.get("Data"))
    player = data.get("Players", [])
    player = player[0]
    return player["Name"]
while message["Event"] != "UpdateState":
    time.sleep(0.1)
    message = client.get_message()
with open("player_name.txt", "w") as file:
    file.write(get_name(message))

with open("last_ball_data.txt", "w") as file:
    file.write(f"0,0,0,0,0,")
with open("last_player_data.txt", "w") as file:
    file.write(f"0,0,0,0,0,0,0,0,0,0,0,")

def collect_data():
    with open("last_player_data.txt", "r") as file:
        data = file.read()
        data = data[:-1]
        data = data.split(",")
    row = data
    with open("last_ball_data.txt", "r") as file:
        data = file.read()
        data = data[:-1]
        data = data.split(",")
    row += data
    with open("data.txt", "a") as file:
        for each in row:
            file.write(f"{each},")
        file.write(f"\n")

def get_ball_data(message):
    data = json.loads(message.get("Data"))
    ball = data["Ball"]
    location = ball["Location"]
    datums = []
    player = data["Players"][0]
    with open("player_name.txt", "r") as file:
        player_of_interest = file.read()
    datums = [int(player["Name"] == player_of_interest), round(ball["PreHitSpeed"], 2), round(ball["PostHitSpeed"], 2), round(location["X"], 2), round(location["Y"], 2), round(location["Z"], 2)]
    with open("last_ball_data.txt", "w") as file:
        for each in datums:
            file.write(f"{each},")

def get_player_data(message):
    data = json.loads(message.get("Data"))
    player = data.get("Players", [])
    player = player[0]
    game = data.get("Game")
    ball = game["Ball"]
    datums = []
    if "Touches" in player:
        datums.append(player["Touches"])
    else:
        datums.append(int(False))
    if "Speed" in player:
        datums.append(round(player["Speed"], 2))
    else:
        datums.append(int(False))
    if "Boost" in player:
        datums.append(player["Boost"])
    else:
        datums.append(int(False))
    if "bBoosting" in player:
        datums.append(int(True))
    else:
        datums.append(int(False))
    if "bOnGround" in player:
        datums.append(int(True))
    else:
        datums.append(int(False))
    if "bOnWall" in player:
        datums.append(int(True))
    else:
        datums.append(int(False))
    if "bPowersliding" in player:
        datums.append(int(True))
    else:
        datums.append(int(False))
    if "bSupersonic" in player:
        datums.append(int(True))
    else:
        datums.append(int(False))
    if "Speed" in ball:
        datums.append(round(ball["Speed"], 2))
    else:
        datums.append(int(False))
    if "TeamNum" in ball:
        datums.append(int(ball["TeamNum"] == player["TeamNum"]))
    else:
        datums.append(int(False))

    with open("last_player_data.txt", "w") as file:
        for each in datums:
            file.write(f"{each},")


def on_press(key):
    if key == KeyCode.from_char("p"):
        collect_data()
        with open("labels.txt", "a") as file:
            file.write(f"{str(1)}\n")
    if key == KeyCode.from_char("o"):
        collect_data()
        with open("labels.txt", "a") as file:
            file.write(f"{str(0)}\n")

listener = keyboard.Listener(on_press=on_press)
listener.start()


def main():
    last_message = client.get_message()

    if last_message["Event"] == "BallHit":
        get_ball_data(last_message)
    if last_message["Event"] == "UpdateState":
        get_player_data(last_message)


if __name__ == "__main__":
    while True:
        main()
