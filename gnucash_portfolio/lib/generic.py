"""
Generic utilities
"""
import tempfile
import time
import os
import webbrowser
from datetime import datetime, timedelta
#from functools import partial
from sqlalchemy.dialects import sqlite
from gnucash_portfolio.lib import settings, generic


def get_today():
    """
    Returns the current date string in ISO format.
    """
    return get_date_iso_string(time)


def get_yesterday():
    """
    Returns yesterday's datetime
    """
    return datetime.today() - timedelta(days=1)

def get_date_iso_string(value: datetime):
    """ Gets the iso string representation of the given date """
    return value.strftime("%Y-%m-%d")


def print_sql(query):
    """ prints alchemy sql command for debugging """
    sql = str(query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))
    print(sql)
    

def save_to_temp(content, file_name=None):
    """Save the contents into a temp file."""

    #output = "results.html"
    temp_dir = tempfile.gettempdir()
    #tempfile.TemporaryDirectory()
    #tempfile.NamedTemporaryFile(mode='w+t') as f:
    out_file = os.path.join(temp_dir, file_name)
    #if os.path.exists(output) and os.path.isfile(output):
    f = open(out_file, 'w')
    f.write(content)
    f.close()
    #print("results saved in results.html file.")
    #return output
    #output = str(pathlib.Path(f.name))
    return out_file


def read_book_uri_from_console():
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
    output = generic.save_to_temp(result, output_file_name)
    webbrowser.open(output)
