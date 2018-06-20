import random, json, os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from utils import *



app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.secret_key = os.getenv('SECRET_KEY')


class counter:
    attempts = 0
    step = 0
    points_per_q = 10
    total_points = 0
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        
        username = request.form['username']
        clear_counter()
        counter.step = 0
        counter.total_points = 0
        
        if not username: 
            flash('Please fill out username field')
            return redirect(url_for('index'))
        else:
            with open('data/username.json', 'r') as user_data:
                user_data = json.load(user_data)
                user_to_json(user_data, username)
            
            with open('data/qa.json', 'r') as json_data:
                data = json.load(json_data)
                random.shuffle(data)
                five_random_q = data[:5]
                
            with open('data/five_questions.json', 'w') as five_q:
                json.dump(five_random_q, five_q, indent=2)
            
            return redirect(request.form['username'])
        
    return render_template('index.html')


@app.route('/<username>', methods=["GET", "POST"])
def questions(username):
    
    with open('data/five_questions.json', 'r') as json_data:
        data = json.load(json_data)
        
    if request.method == "POST":
        score = quiz_answer(data)
        
        # Action on skip button
        if request.form.get("Skip question"):
            counter.attempts = 0
            counter.points_per_q = 10
            if counter.step < 4:
                counter.step += 1
                return render_template('questions.html', username = username, data = data[counter.step], step = counter.step, q_points = counter.points_per_q)
            else:
                counter.step = 4
                total = counter.total_points
                append_user_result_in_data(username, total)
                return redirect(url_for('result', username = username, score = score, total = total))
        
        # Action if empty input field
        if request.form['answer'] == '':
            flash("Please fill the answer")
            return render_template('questions.html', username = username, data = data[counter.step], step = counter.step, q_points = counter.points_per_q)
        
        # Action when correct answer
        if correct_answer(data):
            counter.total_points += counter.points_per_q
            counter.points_per_q = 10
            
            if counter.step < 4:
                counter.attempts = 0
                if counter.step < 4:
                    counter.step += 1
                else:
                    counter.step = 4
                return render_template('questions.html', username = username, data = data[counter.step], step = counter.step, q_points = counter.points_per_q)
            else:
                total = counter.total_points
                append_user_result_in_data(username, total)
                return redirect(url_for('result', username = username, score = score, total = total))
                
        # Action when wrong answer
        else:
            counter.attempts += 1
            if counter.attempts < 5:
                flash("Wrong answer! Try again")
                counter.points_per_q -= 2
                return render_template('questions.html', username = username, data = data[counter.step], step = counter.step, q_points = counter.points_per_q)
            else:
                counter.points_per_q = 10
                if counter.step < 4:
                    counter.attempts = 0
                    if counter.step < 4:
                        counter.step += 1
                    else:
                        counter.step = 4
                return render_template('questions.html', username = username, data = data[counter.step], step = counter.step, q_points = counter.points_per_q)
            
        
    return render_template('questions.html', data = data[0], username = username, step = counter.step, q_points = counter.points_per_q)



@app.route('/result')
def result():
    
    score = request.args.get('score')
    username= request.args.get('username')
    
    total= request.args.get('total')
    
    with open('data/username.json', 'r') as data:
        data = json.load(data)
        #newlist = sorted(data, key=itemgetter('score'), reverse=True)
        data.sort(key=lambda e: e['user']['score'], reverse=True)
        
    return render_template('result.html', data = data, username= username, score = score, total = total)
        
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
