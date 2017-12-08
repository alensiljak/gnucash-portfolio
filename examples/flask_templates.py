"""
Demonstrates use of templates and template inheritance with Flask
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Default view/route"""
    return render_template('child_template.html')

if __name__ == '__main__':
    app.run()
