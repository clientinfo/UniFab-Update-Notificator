"""
Module: console_color

This module defines a Color class that provides ANSI escape sequences
for color formatting in terminal outputs.
"""


class Color:
    """
    A class providing ANSI escape sequences for color formatting in terminals.
    """

    BLUE = "\033[34m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    @staticmethod
    def blue(arg_text):
        """
        Formats text in blue color.

        Args:
            arg_text (str): The text to format.

        Returns:
            str: The formatted text in blue color.
        """
        return f"{Color.BLUE}{arg_text}{Color.RESET}"

    @staticmethod
    def red(arg_text):
        """
        Formats text in red color.

        Args:
            arg_text (str): The text to format.

        Returns:
            str: The formatted text in red color.
        """
        return f"{Color.RED}{arg_text}{Color.RESET}"

    @staticmethod
    def green(arg_text):
        """
        Formats text in green color.

        Args:
            arg_text (str): The text to format.

        Returns:
            str: The formatted text in green color.
        """
        return f"{Color.GREEN}{arg_text}{Color.RESET}"
