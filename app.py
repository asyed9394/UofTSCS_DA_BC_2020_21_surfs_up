from flask import Flask
app = Flask(__name__)
#define root route
@app.route('/')
#function that will go into the rout
def hello_world():
    return "Hello World"
#Skill drill Think of some simple route and then try to reate the route and implement the logic
@app.route('/my_test')
def my_logic():
    message =  f"This is my testing route.<br/>"\
          f"Try printing different lines"
    return message