""" File helpers """

def read_text_from_file(path: str) -> str:
    """ Reads text file contents """
    with open(path) as text_file:
        content = text_file.read()

    return content

def save_text_to_file(content: str, path: str):
    """ Saves text to file """
    with open(path, mode='w') as text_file:
        text_file.write(content)
