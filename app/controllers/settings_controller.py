"""
Editor for settings
"""
try: import simplejson as json
except ImportError: import json
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import generic, fileutils
from gnucash_portfolio.lib.settings import Settings


settings_controller = Blueprint( # pylint: disable=invalid-name
    'settings_controller', __name__, url_prefix='/settings')
SETTINGS_FILE_PATH = 'config/settings.json'


@settings_controller.route('/edit')
def edit():
    """ Edit the global settings """
    # load json file
    settings = Settings()
    content = settings.dumps()

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

    settings = Settings()
    settings.loads(content)
    # validate json
    if settings.data:
        # save to file
        settings.save()
        #fileutils.save_text_to_file(content, SETTINGS_FILE_PATH)
        model["message"] = "Saved"
    else:
        model["message"] = "Invalid JSON"

    return render_template('settings.confirmation.html', model=model)
