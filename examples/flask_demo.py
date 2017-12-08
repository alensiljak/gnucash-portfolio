"""
Demonstrate web page with Flask
"""
from flask import Flask
app = Flask(__name__)
from flask import render_template

#from app import routes
#from app import app

@app.route('/')
#@app.route('/index')
def index():
    """Default output"""
    user = { 'nickname': 'Miguel' }
    #return "Hello, World!"
    return render_template('web_flask_demo.html',
                            title='Home',
                            user=user)

if __name__ == "__main__":
    app.run()
