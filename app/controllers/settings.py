"""
Editor for settings
"""
from flask import Blueprint, request, render_template
import json
from gnucash_portfolio.lib import generic


settings_controller = Blueprint('settings_controller', __name__, url_prefix='/settings')
settings_file_path = '../config/settings.json'


@settings_controller.route('/edit')
def edit():
    """ Edit the global settings """
    # load json file
    content = generic.load_json_file_contents(settings_file_path)

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
        with open(settings_file_path, mode='w') as file:
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
