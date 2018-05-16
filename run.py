import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret key"

def randomQuestionsList(data_len, data):
    """
    Generate list of first 5 random numbers of data length
    """
    random_list = range(data_len)
    random.shuffle(random_list)
    
    list = []
    
    for number in random_list[:5]:
        list.append(data[number])
        
    return list
    
    
def getAnswers(data):
    formData = request.form
    
    list = []
    
    randomData = randomQuestionsList(len(data), data)
    for val in formData.values():
        for i in range(0, 5):
            if val == randomData[i].get('answer'):
                list.append(val)
        
    return list            

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        return redirect(request.form['username'])
        
    return render_template('index.html')
    

@app.route('/<username>', methods=["GET", "POST"])
def questions(username):
    with open('data/qa.json', 'r') as json_data:
        data = json.load(json_data)
            
    if request.method == "POST":
        flash(getAnswers(data))
        
    return render_template('questions.html', questions=randomQuestionsList(len(data), data), username = username)


@app.route('/result')
def result():
    return render_template('result.html')
        
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
