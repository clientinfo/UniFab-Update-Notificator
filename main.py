"""
Module: changelog_watcher

This module implements the ChangelogWatcher class, which monitors a specified URL for updates,
parses the changelog, and sends notifications to a Discord webhook.
"""

import time
from modules.console_color import Color  # Import the Color class for color formatting
from modules.changelog_parser import ChangelogParser
from modules.discord_notifier import DiscordNotifier


class ChangelogWatcher:
    """
    ChangelogWatcher class monitors a specified URL for updates,
    parses the changelog, and sends notifications to a Discord webhook.
    """

    def __init__(self, arg_url, arg_webhook_url):
        """
        Initializes the ChangelogWatcher instance with the provided URL and Discord webhook URL.

        Args:
            arg_url (str): The URL to fetch the changelog from.
            arg_webhook_url (str): The URL of the Discord webhook to send notifications to.
        """
        self.url = arg_url
        self.webhook_url = arg_webhook_url
        self.discord_notifier = DiscordNotifier(arg_webhook_url)
        self.changelog_parser = ChangelogParser()
        self.last_sent_changelog = self.changelog_parser.load_last_sent_changelog()

    def fetch_changelog(self):
        """
        Fetches the changelog HTML content from the specified URL.

        Returns:
            str or None: The fetched HTML content if successful, None if an error occurs.
        """
        return self.changelog_parser.fetch_changelog(self.url)

    def parse_changelog(self, arg_html_content):
        """
        Parses the HTML content of the changelog to extract version, date, and changelog items.

        Args:
            arg_html_content (str): The HTML content of the changelog to parse.

        Returns:
            dict or None: A dictionary containing version, date, and changelog items
                          if parsing is successful, None if an error occurs.
        """
        return self.changelog_parser.parse_changelog(arg_html_content)

    def send_to_discord_webhook(self, arg_software_name, arg_changelog_data):
        """
        Sends the parsed changelog data to the Discord webhook.

        Args:
            arg_software_name (str): The name of the software for the update.
            arg_changelog_data (dict): The parsed changelog data to send.
        """
        self.discord_notifier.send_to_discord_webhook(arg_software_name, arg_changelog_data)

    def run(self):
        """
        Runs the ChangelogWatcher to continuously monitor the changelog, parse updates,
        and send notifications to Discord.
        """
        while True:
            html_content = self.fetch_changelog()
            if html_content:
                changelog_data = self.parse_changelog(html_content)

                if changelog_data:
                    if changelog_data != self.last_sent_changelog:
                        self.send_to_discord_webhook("UniFab", changelog_data)
                        self.last_sent_changelog = changelog_data
                        self.changelog_parser.save_last_sent_changelog(changelog_data)  # Save immediately
                    else:
                        self.last_sent_changelog = changelog_data
                        self.changelog_parser.save_last_sent_changelog(changelog_data)  # Save immediately
                else:
                    print(Color.red("No valid Update data found."))
            else:
                print(Color.red("Failed to fetch Update data."))

            time.sleep(20)  # 20 seconds


if __name__ == "__main__":
    URL = 'https://de.unifab.ai/unifab-new.htm'  # Replace with the actual URL
    WEBHOOK_URL = ('WEBHOOK URL HERE')
    SOFTWARE_NAME = 'UniFab Update Notificator'
    AUTHOR_NAME = 'clientinfo'

    # Print software name in green and author name in blue
    print(f"{Color.green('Software:')} {Color.blue(SOFTWARE_NAME)}")
    print(f"{Color.green('Creator:')} {Color.blue(AUTHOR_NAME)}")

    watcher = ChangelogWatcher(URL, WEBHOOK_URL)
    watcher.run()
