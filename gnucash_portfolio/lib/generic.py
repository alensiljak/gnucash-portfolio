"""
Generic utilities
"""
import tempfile
import time
try: import simplejson as json
except ImportError: import json
from logging import log, ERROR
import os
import webbrowser
from datetime import datetime, timedelta
from sqlalchemy.dialects import sqlite
from gnucash_portfolio.lib import settings, fileutils


def load_json_file_contents(path: str) -> str:
    """ Loads contents from a json file """
    assert isinstance(path, str)
    content = None

    file_path = os.path.abspath(path)
    content = fileutils.read_text_from_file(file_path)
    json_object = json.loads(content)
    content = json.dumps(json_object, sort_keys=True, indent=4)

    return content

def validate_json(data: str):
    """ Validate JSON by parsing string data. Returns the json dict. """
    result = None
    try:
        result = json.loads(data)
    except ValueError as error:
        log(ERROR, "invalid json: %s", error)

    return result

def print_sql(query):
    """ prints alchemy sql command for debugging """
    sql = get_sql(query)
    print(sql)

def get_sql(query):
    """ Returns the sql query """
    sql = str(query.statement.compile(dialect=sqlite.dialect(),
                                      compile_kwargs={"literal_binds": True}))
    return sql

def save_to_temp(content, file_name=None):
    """Save the contents into a temp file."""

    #output = "results.html"
    temp_dir = tempfile.gettempdir()
    #tempfile.TemporaryDirectory()
    #tempfile.NamedTemporaryFile(mode='w+t') as f:
    out_file = os.path.join(temp_dir, file_name)
    #if os.path.exists(output) and os.path.isfile(output):
    file = open(out_file, 'w')
    file.write(content)
    file.close()
    #print("results saved in results.html file.")
    #return output
    #output = str(pathlib.Path(f.name))
    return out_file

def read_book_uri_from_console():
    """ Prompts the user to enter book url in console """
    db_path: str = input("Enter book_url or leave blank for the default settings value: ")
    if db_path:
        # sqlite
        if db_path.startswith("sqlite://"):
            db_path_uri = db_path
        else:
            # TODO: check if file exists.
            db_path_uri = "file:///" + db_path
    else:
        cfg = settings.Settings()
        db_path_uri = cfg.database_uri

    return db_path_uri

def run_report_from_console(output_file_name, callback):
    """
    Runs the report from the command line. Receives the book url from the console.
    """
    print("The report uses a read-only access to the book.")
    print("Now enter the data or ^Z to continue:")

    #report_method = kwargs["report_method"]
    result = callback()

    #output_file_name = kwargs["output_file_name"]
    output = save_to_temp(result, output_file_name)
    webbrowser.open(output)
