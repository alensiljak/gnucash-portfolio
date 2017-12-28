"""
Editor for settings
"""
try: import simplejson as json 
except ImportError: import json
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import generic


settings_controller = Blueprint( # pylint: disable=invalid-name
    'settings_controller', __name__, url_prefix='/settings')
SETTINGS_FILE_PATH = 'config/settings.json'


@settings_controller.route('/edit')
def edit():
    """ Edit the global settings """
    # load json file
    content = generic.load_json_file_contents(SETTINGS_FILE_PATH)

    # display in text editor for now
    model = {
        "title": "Settings",
        "content": content
    }
    return render_template('content.editor.html', model=model)


@settings_controller.route('/edit', methods=['POST'])
def save():
    """ Save the settings """
    model = {
        "message": "Saved"
    }
    content: str = request.form.get('content')

    # validate json
    if json_validate(content):
        json_object = json.loads(content)
        # clean-up and format
        content = json.dumps(json_object)
        # save to file
        with open(SETTINGS_FILE_PATH, mode='w') as file:
            file.write(content)
            model["message"] = "Saved"
    else:
        model["message"] = "Invalid JSON"

    return render_template('settings.confirmation.html', model=model)


def json_validate(data):
    """ Validate JSON """
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False
