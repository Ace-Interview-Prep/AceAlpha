from flask import render_template, request, redirect
import random
from os import environ, path, makedirs
from forms import RegisterForm
from flask_lambda import FlaskLambda
import boto3

#for simplification use .resource and not .client which leads to a large JSON object

#Change ENV HERE
baseAPI = "https://5a6996u1hc.execute-api.ca-central-1.amazonaws.com/Prod"  # lamdba or API Gateway ref 

app = FlaskLambda(__name__, instance_relative_config=False, static_folder="static", template_folder="templates")
app.secret_key='SOmeBulshtiachen32xe'

@app.route('/form/', methods=['GET', 'POST'])
def first_form():
  form = RegisterForm()
  name = form.name.data
  email = form.email.data
  job_type = form.job_types.data 
  if form.validate_on_submit():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    table.put_item(
      Item = {
        'name': name,
        'email': email,
        'job_type': job_type
      }
    )

    return redirect(baseAPI + '/recorder/' + email + '/' + job_type + '/')
  return (
      render_template('emailForm.html', form=form),
      200,
      {'Content-Type': 'text/html'}
  )
    

@app.route('/recorder/<email>/<job_type>/', methods=['GET', 'POST']) #get rid of page use ;+ redirect to thank you page through JS
def video_html(email, job_type): #x is their email
    roleQuestions = getQuestions(job_type)
    generalQuestions = ["Tell me about yourself.",
                        "What are your strengths and weaknesses?", 
                        "Why do you want to work here? (Pick your ideal company)",
                        "What interests you about this role?",
                        "What motivates you?",
                        "What are you passionate about?",
                        "Why are you leaving your current job?",
                        "What did you like most about your last position? Least?",
                        "What is your teaching philosophy?",
                        "What are your long-term goals?"]

    s3 = boto3.resource('s3')
    # needs to be updated 
    video_data_bytes = request.get_data()
    print(video_data_bytes[:100])

    if len(video_data_bytes) != 0:  
    #put video in S3 bucket
        filename = email +'/videofile' + str(random.randint(1,1000000)) + '.mp4'
        s3.Bucket('aceuploadsbucket').put_object(Key=filename, Body=video_data_bytes)

    
    return (
        render_template('test-shit.html', email=email, base=baseAPI, generalQuestions=generalQuestions, job_type=job_type, roleQuestions=roleQuestions),
        200,
        {'Content-Type': 'text/html'}
    ) 
  

def getQuestions(job_type):
  questions = {
    "Software_Developer": [
      "Tell me about a tough software development problem you've taken on, and how you solved it.",
      "What obstacles have you run into while working on a software project, and how did you deal with them?",
      "Are you working on a passion project? What is it?",
      "What is your favourite language, tool, or library to use and why?",
      "If you had to describe to someone your problem solving approach that you take when starting on a brand new problem what would you say?",
      "There was an article that a great developer can have the same effect as a team of 5 average developers. If you had to guess, how could that be?",
      "What started your interest in coding?",
      "Tell me about a time you worked through a communication issue when working with a stakeholder? (OR) : If you haven’t been a part of communicating with stakeholders, communication issues with project managers",
      "Tell me about a time when you learned something about coding from normal day-to-day life",
      "What is something you want to learn about? Doesn’t have to be coding focused"
    ],
    "Designer": [
      "As a Designer, sometimes you will be given a large scope of work upfront, how do you typically begin on a project?",
      "Do you have any sources of inspiration for your work? Who/what are they?",
      "Tell us about a time you had to communicate your knowledge of design to another profession",
      "When you’ve worked in a team before, how would you describe what your role ended up being? How did that complement the rest of the team?",
      "What is your favourite product ever? What is the first thing you would change about it?",
      "Walk me through the project that you most enjoyed working on and tell me why it’s important/would be important to its intended user",
      "If you were to ask the first question ever to your target user, what would you ask and why?"
    ],
    "Product_Manager": [
      "How do your past roles, prior to product management, influence your perspective on what makes a great PM?",
      "What is your main priority at the start of a project?",
      "How would you explain Agile Project Management to someone who believes it is 'just being lazy about planning'"
    ],
    "Sales": [
      "Tell me about a time that you handled an objection from a customer, colleague, or boss",
      "Pick up the closest item to you (notebook, pen, paper, etc.) and sell it to me without selling it as the function it does (i.e. if you choose a pen, you can’t sell it to me as the best writing tool out there)",
      "Tell me about a time that you dealt with an unhappy customer",
      "What motivates you as a sales rep?"
    ],
    "Business_Analyst":[
      "How would you deal with working with difficult stakeholders?",
      "What is the importance of analytical reporting?",
      "Walk me through how you would approach a new project.",
      "What tools do you think a business analyst should prioritize"
    ],
    "Management_Consulting": [
      "How would you calculate how many traffic lights there are in Toronto, ON?",
      "What are your long-term goals?",
      "What do you do for fun?",
      "Tell me about a time when you had to solve a difficult problem? What was your process?",
      "How would you describe your leadership style?",
    ],
    "Finance": [
      "How would you calculate how many traffic lights there are in Toronto, ON?",
      "If you could only choose one profitability model to forecast for your projects, which would it be and why?",
      "Walk me through a time that you have used financial benchmarking.",
      "What financial methodologies are you familiar with for conducting an analysis?",
      "What components would you use to portray the financial health of your company to an investor?",
      "If you could choose one evaluation metric to use when reviewing company stock, which would it be and why?"
    ],
    "Marketing": [
      "What measures of success would you set for a marketing social media campaign?",
      "How would you describe our company brand?",
      "A customer left a negative review of our product on a social media site. How do you respond to the customer?",
      "Tell me about your favourite product. How would you market it?",
      "Tell me about a project you worked on where you had a team of people with different ideas from you. How did you manage the situation?",
      "You have been given a project to re-brand a product that has been performing poorly. How do you approach this?",
      "What are the three most important skills for a marketing career?"
    ],
    "Other": [] #keep empty
  }  
  roleSpecific = questions[job_type] 
  return roleSpecific

@app.route('/thankYouSooooooooooooooooooooooooooooooooooMuch/', methods=['GET'])
def thank_you():
  print(' I WAS CALLED ')
  return (
      render_template('thank_you.html'),
      200,
      {'Content-Type': 'text/html'}
  ) 
  