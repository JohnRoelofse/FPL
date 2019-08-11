from flask import Flask, render_template
from gameweek_captains import captains
app = Flask(__name__)

@app.route('/')
def index():
    captain = captains()
    return render_template('welcome_page.html', captain = captain)