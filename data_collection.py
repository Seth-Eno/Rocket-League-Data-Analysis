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

def collect_player_data(message, last_ball_hit):
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
        datums.append(ball["Speed"])
    else:
        datums.append(int(False))
    if "TeamNum" in ball:
        datums.append(int(ball["TeamNum"] == player["TeamNum"]))
    else:
        datums.append(int(False))



    with open("data.txt", "a") as data:
        for datum in datums:
            data.write(f"{datum}, ")
        data.write(f"\n")




def main():
    last_message = client.get_message()
    last_ball_hit = [[], 0, 0, 0, 0, 0]

    if last_message["Event"] == "UpdateState":
        collect_player_data(last_message, last_ball_hit)

    if last_message["Event"] == "BallHit":
        data = json.loads(last_message.get("Data"))
        ball = data["Ball"]
        location = ball["Location"]
        players = []
        for i in range(len(data["Players"])):
            players.append(data["Players"][i]["Name"])
        last_ball_hit = [players, ball["PreHitSpeed"], ball["PostHitSpeed"], location["X"], location["Y"], location["Z"]]


if __name__ == "__main__":
    while True:
        main()
