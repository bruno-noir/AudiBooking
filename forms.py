from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TimeField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4,max=40)])
    submit = SubmitField('Send OTP')

class OTP(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired(), Length(min=6,max=6)])
    submit = SubmitField('Login')

class Register(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=2,max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4,max=40)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AddExpenses(FlaskForm):
    details = StringField('Expenses Details', validators=[DataRequired(), Length(min=2,max=30)])
    amount = StringField('Expenses Amount', validators=[DataRequired()])
    submit = SubmitField('Add Expenses')

class Show(FlaskForm):
    name = StringField('Show Name', validators=[DataRequired(), Length(min=2,max=40)])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    ordinary_seats = IntegerField('Number of Ordinary Seats', validators=[DataRequired()])
    o_price = IntegerField('Price of Ordinary Seats', validators=[DataRequired()])
    balcony_seats = IntegerField('Number of Balcony Seats', validators=[DataRequired()])
    b_price = IntegerField('Price of Balcony Seats', validators=[DataRequired()])
    submit = SubmitField('Add Show')

class SearchShow(FlaskForm):
    show_name = StringField('Show Name')
    submit = SubmitField('Find Show')