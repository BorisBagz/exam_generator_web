from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, QuestionForm, ScoreForm
import json
import random

# GLOBAL VARIABLES
number_questions = 5        #number of questions we want to ask
questions_made = []         #array with the index of the questions already answered
answers = []                #array with the good and given answers
valid_answers = ['a', 'b', 'c', 'd']    #array with the valid options as answers
valid_exams = ['CCSA R80']
json_questions = 'questions/questions-ccsa.json'
passing_score = 71
points = 0
asked_questions = []


def read_json_file(json_file):
    with open(json_file) as questions_file:
        data = json.load(questions_file)
        return data

#check if the random generated number used as
#index for the questions was not already asked
#if it is indeed new, we append the question to the array questions_made
def check(my_number):
    if my_number not in questions_made:
        questions_made.append(my_number)
        return True

#generate a random number between 0 and the total number of questions in the json
#then checks if it was not asked yet
def generate(length):
    while True:
        my_number = random.randint(0,length)
        if check(my_number):
            return my_number

#check if the given answer is a,b,c or d (appears in valid_answers)
def validate_answer(my_answer):
    if my_answer in valid_answers:
        return True
    else:
        return False

#fetch the input from the user
#while true (do while loop) to check if the input is a b c or d
#in that case, add the given answer along with the good answer to the answers array
#return the given answer
#otherwise ask the option again
def answering(my_answer):
    if validate_answer(my_answer):
        answers.append(my_answer)
        return True
    else:
        return False

@app.route('/questions')
def print_questions():
    data = read_json_file(json_questions)
    length = len(data)
    return render_template('questions.html', questions=data, length=length)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        exam_number = form.exam_id.data
        exam_name = ''
        if exam_number == '1':
            exam_name = 'CCSA R80'
        flash('Exam requested for user {} and test {}'.format(form.username.data, exam_name))
        return redirect('/question')
    return render_template('index.html', title='Welcome', form=form)

@app.route('/question', methods=['GET', 'POST'])
def question():
    global points
    form_quest = QuestionForm()
    form_score = ScoreForm()
    data = read_json_file(json_questions)
    length = len(data) - 1
    while len(questions_made) < number_questions:
        random_index = generate(length)
        asked_questions.append(data[random_index])
        good_answer = data[random_index]['answer']
        if form_quest.validate_on_submit():
            my_answer = form_quest.answer.data
            if answering(my_answer):
                if my_answer == good_answer:
                    points += 1
                redirect('/question')
        return render_template('question.html', question=data[random_index], form=form_quest)
    if form_score.validate_on_submit():
        correction = form_score.corrections.data
        if correction == 'Yes' :
            return render_template('score.html', points=points, num_questions=number_questions,
                                                 corrections=correction, questions=asked_questions,
                                                 form=form_score)
    return render_template('score.html', points=points, num_questions=number_questions, form=form_score)

if __name__ == "__main__":
    app.run()
