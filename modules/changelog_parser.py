"""
Module: changelog_parser

This module provides functionality to fetch, parse, save, and load changelog data
from HTML and JSON files.
"""

import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from modules.console_color import Color  # Import the Color class from console_color.py


class ChangelogParser:
    """
    A class to fetch, parse, save, and load changelog data from HTML and JSON files.

    Methods:
        fetch_changelog(arg_url):
            Fetches HTML content from a given URL.

        parse_changelog(arg_html_content):
            Parses HTML content to extract changelog information.

        save_last_sent_changelog(arg_changelog_data):
            Saves parsed changelog data to a JSON file.

        load_last_sent_changelog():
            Loads previously saved changelog data from a JSON file.
    """

    @staticmethod
    def fetch_changelog(arg_url):
        """
        Fetches HTML content from a given URL using requests.

        Args:
            arg_url (str): The URL to fetch HTML content from.

        Returns:
            str: The HTML content fetched from the URL, or None if there was an error.
        """
        try:
            response = requests.get(arg_url, timeout=10)  # Added timeout argument
            response.raise_for_status()  # Raise an error for bad status codes
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Fetching URL:')} {arg_url}")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Error fetching the URL:')} {e}")
            return None

    @staticmethod
    def parse_changelog(arg_html_content):
        """
        Parses HTML content to extract changelog information using BeautifulSoup.

        Args:
            arg_html_content (str): The HTML content to parse.

        Returns:
            dict or None: A dictionary containing parsed changelog data (version, date, changelog),
                          or None if parsing fails or no valid changelog data found.
        """
        if not arg_html_content:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Empty HTML content received.')}")
            return None

        try:
            soup = BeautifulSoup(arg_html_content, 'html.parser')
            container = soup.find('div', class_='bg-white b-rd-8 pl40 pr40 pb32 changelog-content')
            if not container:
                print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                      f"{Color.red('Container div not found.')}")
                return None

            section = container.find('p', class_='whatsnew')
            if not section:
                print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                      f"{Color.red('No changelog section found within the container.')}")
                return None

            version = section.find('strong').text.strip() if section.find('strong') else 'N/A'
            date = section.find('span').text.strip() if section.find('span') else 'N/A'
            changelog_items = section.find_all('li')
            changelog = [item.text.strip() for item in changelog_items]
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.green('Changelog data parsed successfully.')}")
            return {
                'version': version,
                'date': date,
                'changelog': changelog
            }
        except ValueError as ve:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('ValueError parsing HTML content:')} {ve}")
            return None
        except AttributeError as ae:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('AttributeError parsing HTML content:')} {ae}")
            return None
        except Exception as e:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Error parsing HTML content:')} {e}")
            return None

    @staticmethod
    def save_last_sent_changelog(arg_changelog_data):
        """
        Saves parsed changelog data to a JSON file named 'last_sent_changelog.json'.

        Args:
            arg_changelog_data (dict): The changelog data to save.
        """
        try:
            with open('last_sent_changelog.json', 'w', encoding='utf-8') as file:  # Specified encoding
                json.dump(arg_changelog_data, file, indent=4)  # Update the file with indent for readability
                print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                      f"{Color.green('Changelog data saved to file.')}")
        except FileNotFoundError as fnfe:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('FileNotFoundError saving Changelog data:')} {fnfe}")
        except IOError as ioe:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('IOError saving Changelog data:')} {ioe}")
        except Exception as e:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Error saving Changelog data:')} {e}")

    @staticmethod
    def load_last_sent_changelog():
        """
        Loads previously saved changelog data from 'last_sent_changelog.json'.

        Returns:
            dict or None: A dictionary containing the last sent changelog data,
                          or None if the file doesn't exist or cannot be loaded.
        """
        try:
            if os.path.exists('last_sent_changelog.json'):
                with open('last_sent_changelog.json', 'r', encoding='utf-8') as file:  # Specified encoding
                    last_sent_changelog = json.load(file)
                    print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                          f"{Color.green('Last sent changelog data loaded from file.')}")
                    return last_sent_changelog
            else:
                print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                      f"{Color.red('No saved changelog data found. Creating a new file.')}")
                with open('last_sent_changelog.json', 'w', encoding='utf-8') as file:  # Specified encoding
                    json.dump(None, file)  # Create an empty JSON object
                    print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                          f"{Color.green('Empty file created for the last sent changelog data.')}")
                    return None
        except FileNotFoundError as fnfe:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('FileNotFoundError loading last sent changelog data:')} {fnfe}")
        except IOError as ioe:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('IOError loading last sent changelog data:')} {ioe}")
        except json.JSONDecodeError as je:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('JSONDecodeError loading last sent changelog data:')} {je}")
        except Exception as e:
            print(f"{Color.blue('[' + datetime.now().strftime('%H:%M:%S') + ']')}: "
                  f"{Color.red('Error loading last sent changelog data:')} {e}")
            return None
