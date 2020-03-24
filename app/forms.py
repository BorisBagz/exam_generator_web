from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    exam_id = StringField('ExamID', validators=[DataRequired()])
    submit = SubmitField('Start your Exam!')

class QuestionForm(FlaskForm):
    answer = SelectField('Your Answer', choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], validators=[DataRequired()])
    submit_question = SubmitField('Send your answer')

class ScoreForm(FlaskForm):
    corrections = SelectField('Corrections', choices=[('Yes', 'Y'), ('No', 'N')], validators=[DataRequired()])
    submit_correction = SubmitField('Send')
