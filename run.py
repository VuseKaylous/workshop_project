from flask import Flask, request
# from flask_ngrok import run_with_ngrok
import subprocess
from io import StringIO

app = Flask(__name__)
# run_with_ngrok(app)

form_template = """
        <h1>Input: List of control points</h1>
        <form method="POST" enctype = "multipart/form-data">
            <textarea id = "input" name = "input" rows="10" cols="50"></textarea>
            <br>
            <input type = "submit" value = "Submit"/>
        </form>
        """
output_place = '<br><p id="output">'

def handle_input(outputs):
    split_line = outputs.split('\n')
    arr = []
    for s in split_line:
        temp = s.strip().split()
        for i in range(len(temp)):
            temp[i] = float(temp[i])
        arr.append(temp)
    return arr

@app.route("/", methods = ['GET', 'POST'])
async def home():
    inputs = ""
    if request.method == 'POST':
        inputs = request.form['input']
        output = inputs.split('\n')
        print(handle_input(inputs))
        # you handle the input here
    return form_template + output_place + inputs + "</p>"


    
app.run()
