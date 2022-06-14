from rcon.source import Client
import time
from discord_webhook import DiscordWebhook

def main():
    previous_response = None
    previous_player_count = None
    while True:
        with Client('factorio.i.graysonhead.net', 25575, passwd='$GAME_PASSWORD') as client:
            response = client.run('/players', 'online')
        player_count = response[response.find('(')+1:response.find(')')]
        if response != previous_response and previous_response is not None:
            if player_count > previous_player_count:
                content = f"A player has joined the server: \n{response}"
            else:
                content = f"A player has left the server: \n{response}"
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/986093737493012490/xyto8jIU4zmRpVO4CJLKQVm-PWR6NAmvGDvzLEdjcUw3tiXdLWKKpSZyy84Fd8P5kEor",
                content=content
                )
            resp = webhook.execute()
        previous_response = response
        previous_player_count = player_count
        time.sleep(10)

if __name__ == "__main__":
    main()