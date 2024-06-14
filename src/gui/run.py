import os
import sys
from flask import Flask, render_template, request

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/model', methods=["POST"])
def run_model():
    if request.method == "POST":
       a = request.form.get("initial_goats")
       b = request.form.get("initial_age") 
       res = {"alpha":a, "beta":b, "gamma":a+b}
       return res


if __name__ == '__main__':
    app.run(debug=True)

#pyinstaller -F --add-data "templates;templates" --add-data "static;static" run.py