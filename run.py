import random, json, os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret key"


def quiz_answer(data):
    
    count = 0
    
    for i in range(len(request.form)):
        answers = request.form[str(i+1)]
        for j in range(len(data)):
            if answers == data[j]['answer']:
                count += 1
    return count

"""
Function if_user_exist() check username.json data for filled username
If username exist function return true
"""    
def if_user_exist(user_data, username):
    for item in user_data:
        if username in item:
            return True
        
"""
Function user_to_json() create new username data field 
If if_user_exist() return true
"""   
def user_to_json(user_data, username):
    if not if_user_exist(user_data, username):
        with open('data/username.json', 'w') as user:
            user_dict = {username:{'name':username}}
            user_data.append(user_dict)
            json.dump(user_data, user, indent=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        
        username = request.form['username']
        
        if not username: 
            flash('Please fill out username field')
            return redirect(url_for('index'))
        else:
            with open('data/username.json', 'r') as user_data:
                user_data = json.load(user_data)
                user_to_json(user_data, username)
            return redirect(request.form['username'])
        
    return render_template('index.html')
    

@app.route('/<username>', methods=["GET", "POST"])
def questions(username):
    with open('data/qa.json', 'r') as json_data:
        data = json.load(json_data)
        random.shuffle(data)
        
    if request.method == "POST":
        flash('Correct answers {} out of 5'.format(quiz_answer(data)))
        return redirect(url_for('result'))
        
    return render_template('questions.html', data = data[:5], username = username)


@app.route('/result')
def result():
    return render_template('result.html')
        
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
