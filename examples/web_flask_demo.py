"""
Demonstrate web page with Flask
"""
from flask import Flask

app = Flask(__name__)

#from app import routes
#from app import app

@app.route('/')
#@app.route('/index')
def index():
    """Default output"""
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
