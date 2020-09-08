from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, SelectField #, FileField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, URL) 

jobList = [
  ('Designer', 'Designer'),  
  ('Software_Developer', 'Software Developer'),
  #('Data Science', 'Data Science'),
  #('Civil Engineering', 'Civil Engineering'),
  #('Biomedical Engineering', 'Biomedical Engineering'),
  #('Chemical Engineering', 'Chemical Engineering'),
  ('Sales', 'Sales'),
  #('Communications', 'Communications'),
  ('Business_Analyst', 'Business Analyst'),
  #('Accounting', 'Accounting'),
  #('Human Resources', 'Human Resources'),
  #('Legal', 'Legal'),
  #('Educational', 'Educational'),
  ('Management_Consulting', 'Management Consulting'),
  ('Finance', 'Finance'),
  ('Marketing', 'Marketing'),
  ('Other', 'Other')
]

class RegisterForm(FlaskForm):
  name = StringField('Name', [Length(min=1,max=50)])
  #username = StringField('Username', [Length(min=4, max=25)])
  email = StringField('Email',[Length(min=6, max=50)])
  job_types = SelectField(label='Job Type', choices=jobList)
  submit = SubmitField('Submit')
  #password = PasswordField('Password', [
  #    validators.DataRequired(),
  #    validators.EqualTo('confirm', message='Passwords do not match')
  #  ])
  #confirm = PasswordField('Confirm Password')
  


