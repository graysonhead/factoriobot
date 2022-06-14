from rcon.source import Client
import time
from discord_webhook import DiscordWebhook
import os

def main():
    rcon_address = os.getenv["FB_RCON_ADDRESS"]
    rcon_port = os.getenv["FB_RCON_PORT"]
    rcon_password = os.getenv["FB_RCON_PASSWORD"]
    webhook_url = os.getenv["FB_WEBHOOK_URL"]
    previous_response = None
    previous_player_count = None
    while True:
        with Client(rcon_address, int(rcon_port), passwd=rcon_password) as client:
            response = client.run('/players', 'online')
        player_count = response[response.find('(')+1:response.find(')')]
        if response != previous_response and previous_response is not None:
            if player_count > previous_player_count:
                content = f"A player has joined the server: \n{response}"
            else:
                content = f"A player has left the server: \n{response}"
            webhook = DiscordWebhook(
                url=webhook_url,
                content=content
                )
            resp = webhook.execute()
        previous_response = response
        previous_player_count = player_count
        time.sleep(10)

if __name__ == "__main__":
    main()