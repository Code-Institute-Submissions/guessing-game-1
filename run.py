import random, json, os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret key"


def quiz_answer(data):
    count = 0
    
    for i in range(len(request.form)):
        answers = request.form[str(i+1)]
        for j in range(len(data)):
            if answers.lower() == data[j]['answer'].lower():
                count += 1
    return count

"""
Function if_user_exist() check username.json data for filled username
If username exist function return true
"""    
def if_user_exist(user_data, username):
    for item in user_data:
        if username.lower() in item['user']['name']:
            return True
        
"""
Function user_to_json() create new username data field 
If if_user_exist() return true
"""   
def user_to_json(user_data, username):
    if not if_user_exist(user_data, username):
        with open('data/username.json', 'w') as user:
            user_dict = {'user':{'name':username.lower()}}
            user_data.append(user_dict)
            json.dump(user_data, user, indent=2)

"""
Function receive scors and append to data

!!! Save only the best result
"""
def append_user_result_in_data(username, score):
    with open('data/username.json', 'r') as users_data:
        users_data = json.load(users_data)
        
    for item in users_data:
        if username.lower() in item['user']['name']:
            item['user'].update({'score': score}) 
    
    with open('data/username.json', 'w') as user:
        json.dump(users_data, user, indent=2)
                
                

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
        flash(username)
        flash('Correct answers {} out of 5'.format(quiz_answer(data)))

        append_user_result_in_data(username, quiz_answer(data))

        return redirect(url_for('result', username = username))
        
    return render_template('questions.html', data = data[:5], username = username)


@app.route('/result')
def result():
    return render_template('result.html')
    

@app.route('/chartlist')
def chartlist():
    with open('data/username.json', 'r') as data:
        data = json.load(data)
        #newlist = sorted(data, key=itemgetter('score'), reverse=True)
        data.sort(key=lambda e: e['user']['score'], reverse=True)
        
    return render_template('chartlist.html', data = data)
        
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
