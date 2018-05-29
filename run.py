import random, json, os, re
from flask import Flask, render_template, request, redirect, url_for, flash
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)
app.secret_key = "secret key"

step = 0
count = 0

"""
Remove articles from answer
"""  
def remove_articles(text):
    nltk.download('stopwords')
    nltk.download('punkt')
    
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
            
    myList = ' '.join(map(str, filtered_sentence)) 
    
    myList = re.sub(" \,", ",", myList)
    myList = re.sub(" \.", ".", myList)
    
    return myList

"""
Return correct answers per each question
"""  
def quiz_answer(data):
    global count
    for i in range(len(data)):
        
        answers = request.form['1'].lower()
        correct_answer = data[i]['answer'].lower()
        
        if len(answers) != len(correct_answer):
            
            answers = remove_articles(answers)
            
            if not answers:
                count += 0 
            elif not answers.strip():
                count += 0 
            elif answers in correct_answer:
                count += .5
        
        elif answers == correct_answer:
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
        global step 
        global count 
        step = 0
        count = 0
        
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
    #flash(data[0]['answer'])
    if request.method == "POST":
        append_user_result_in_data(username, quiz_answer(data))
        global step 
        if step < 4:
            step += 1
            return render_template('questions.html', username = username, data = data[step])
        else:
            return redirect(url_for('result', username = username, score = quiz_answer(data)))
        
    return render_template('questions.html', data = data[0], username = username)



@app.route('/result')
def result():
    with open('data/username.json', 'r') as data:
        data = json.load(data)
        #newlist = sorted(data, key=itemgetter('score'), reverse=True)
        data.sort(key=lambda e: e['user']['score'], reverse=True)
        
    return render_template('result.html', data = data, username= request.args.get('username'), score = request.args.get('score'))
        
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
