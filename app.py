from flask import Flask, render_template
from gameweek_functions import gameweek_captains
app = Flask(__name__)

@app.route('/')
def index():
    captains = gameweek_captains()
    return render_template('welcome_page.html', captains = captains)

#if __name__ = "__main__":
#    app.run()