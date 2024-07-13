"""
Module: discord_notifier

This module provides functionality to send changelog updates to Discord using webhooks.
"""

import json
from datetime import datetime
import requests
from modules.console_color import Color  # Import the Color class for color formatting


class DiscordNotifier:
    """
    A class to send changelog updates to Discord using webhooks.

    Attributes:
        webhook_url (str): The URL of the Discord webhook to send messages to.
    """

    def __init__(self, arg_webhook_url):
        """
        Initializes a DiscordNotifier instance.

        Args:
            arg_webhook_url (str): The URL of the Discord webhook to send messages to.
        """
        self.webhook_url = arg_webhook_url

    def send_to_discord_webhook(self, arg_software_name, arg_changelog_data):
        """
        Sends a changelog update to Discord using a webhook.

        Args:
            arg_software_name (str): The name of the software being updated.
            arg_changelog_data (dict): The changelog data containing version, date, and changelog details.

        Prints a success message if the update is sent successfully,
        or an error message if there are issues sending the update.
        """
        current_time = datetime.now().strftime('%H:%M:%S')
        if arg_changelog_data:
            try:
                embed_color = 0x00ff00  # Green color (change as needed)
                embed = {
                    'embeds': [{
                        'title': "Latest Update",
                        'description': f"Software: {arg_software_name}\n\n"
                                       f"**Version:** {arg_changelog_data['version']}\n"
                                       f"**Date:** {arg_changelog_data['date']}\n\n"
                                       f"**Changelog:**\n" + "\n".join(
                            f"- {item}" for item in arg_changelog_data['changelog']),
                        'color': embed_color
                    }]
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(self.webhook_url, data=json.dumps(embed), headers=headers, timeout=10)  # Timeout added
                response.raise_for_status()

                print(
                    f"{Color.blue('[' + current_time + ']')}: {Color.green('Changelog sent to Discord successfully.')}")
            except requests.exceptions.RequestException as e:
                print(
                    f"{Color.blue('[' + current_time + ']')}: {Color.red(f'Error sending changelog data to Discord: {e}')}")
        else:
            print(
                f"{Color.blue('[' + current_time + ']')}: {Color.red('No changelog data to send.')}")
