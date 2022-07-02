from rcon.source import Client
import time
from discord_webhook import DiscordWebhook
import os
import re

ONLINE_SEARCH_PATTERN = re.compile('\\s\\s([a-zA-Z0-9]+)\\s\(online\)')



def main():
    rcon_address = os.getenv("FB_RCON_ADDRESS")
    rcon_port = os.getenv("FB_RCON_PORT")
    rcon_password = os.getenv("FB_RCON_PASSWORD")
    webhook_url = os.getenv("FB_WEBHOOK_URL")
    current_players = None

    while True:
        with Client(rcon_address, int(rcon_port), passwd=rcon_password) as client:
            response = client.run('/players', 'online')
        new_list_of_players = ONLINE_SEARCH_PATTERN.findall(response)
        if current_players is None:
            current_players = new_list_of_players
            continue

        new_players = list(
            set(new_list_of_players).difference(current_players)
        )
        lost_players = list(
            set(current_players).difference(new_list_of_players)
        )
        if new_players or lost_players:
            if new_players and not lost_players:
                content = (f"New player(s) joined the server: \n"
                           f"{','.join(new_players)}")
            elif lost_players and not new_players:
                content = (f"Player(s) have left the server: \n"
                           f"{','.join(lost_players)}")
            else:
                content = (f"New player(s): {','.join(new_players)} joined "
                           f"the server and {','.join(lost_players)} left\n")
            webhook = DiscordWebhook(
                url=webhook_url,
                content=content
            )
            resp = webhook.execute()

        current_players = new_list_of_players
        time.sleep(10)


if __name__ == "__main__":
    main()
