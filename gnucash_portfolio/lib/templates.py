"""
Helpers for templates.
"""
import os
import sys

def load_jinja_template(file_name):
    """
    Loads the jinja2 HTML template from the given file.
    Assumes that the file is in the same directory as the script.
    """
    original_script_path = sys.argv[0]
    #script_path = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.dirname(original_script_path)
    # file_path = os.path.join(script_path, file_name)
    # with open(file_path, 'r') as template_file:
    #     return template_file.read()
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template(file_name)

    return template
