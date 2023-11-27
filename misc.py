import re
from sys import exit

def abnormal_termination() -> None:
    """
    Prints an error message and terminates the program.
    """
    print("ERROR: Exit with an error.")
    exit()


def escape_special_chars(text):
    """
    Escapes all non-word and non-space characters in a text string.

    Args:
        text (str): The input string.

    Returns:
        str: The input string with all non-word and non-space characters escaped.

    >>> escape_special_chars("Hello, how are you? I'm fine, thank you!")
    "Hello\\\\, how are you\\\\? I\\\\'m fine\\\\, thank you\\\\!"
    """
    return re.sub(r'([^\w\s])', r'\\\1', text)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
