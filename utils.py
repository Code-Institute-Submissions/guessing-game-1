import nltk, re, json, random, os
from flask import Flask, render_template, request, redirect, url_for, flash
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

count = 0

def clear_counter():
    global count 
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
Addition points for each correct answer
"""  
def quiz_answer(data):
    global count
        
    if correct_answer(data):
        count += 1
    else:
        False
    return count
    

"""
Check if the answer is correct
"""  
def correct_answer(data):
    answer = request.form['answer'].lower()
    for i in range(len(data)):
        
        correct_answer = data[i]['answer'].lower()
        correct_answer = remove_articles(correct_answer)
        answers = remove_articles(answer)
        
        if answers == correct_answer:
            return True
         

"""
Function user_exist() check username.json data for filled username
If username exist function return true
"""    
def user_exist(user_data, username):
    for item in user_data:
        if username.lower() == item['user']['name'].lower():
            return True
        
"""
Function user_to_json() create new username data field 
If user_exist() return true
"""   
def user_to_json(user_data, username):
        
    if not user_exist(user_data, username):
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
        if username.lower() == item['user']['name']:
            item['user'].update({'score': score}) 
    
    with open('data/username.json', 'w') as user:
        json.dump(users_data, user, indent=2)



