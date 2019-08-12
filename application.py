from flask import Flask, render_template
from gameweek_captains import gw_captains
app = Flask(__name__)

@app.route('/')
def index():
    captains = gw_captains()
    return render_template('welcome_page.html', captains = captains)