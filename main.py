import requests
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import time
from chatbot import chat
import pyttsx3
import voicerecognition
from voicerecognition import voice_rec
from nearrestaurants import results

import datetime

now = datetime.datetime.now()


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'

db = SQLAlchemy(app)

class User_table(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	name = db.Column(db.String(80))
	iban = db.Column(db.String(80))
	money = db.Column(db.Integer)
	debts = db.Column(db.Integer)
	weight = db.Column(db.Integer)
	height = db.Column(db.Integer)
	age = db.Column(db.Integer)


	def __init__(self, username, password,name, iban, money, debts, weight, height,age):
		self.username = username
		self.password = password
		self.name = name
		self.money = money 
		self.iban= iban
		self.debts =debts
		self.weight = weight
		self.height = height
		self.age = age

class Message(db.Model):
    #message
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(250))
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    user = db.Column(db.Integer)


engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
	if voice.languages[0] == u'en_US':
		engine.setProperty('voice', voice.id)
		break
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-60)

allow_speak = False

def check_str(line):
	if line == 'Homepage_link':
		return '/'
	if line == 'Healthpage_link':
		return '/health'
	if line == 'Bankpage_link':
		return '/bank'
	if line =='Officepage_link':
		return '/office'
	if line =='Calendar_link':
		return '/calendar'
	if line =='traficpage_link':
		return '/traffic'

	return 'nu'



def speak():
	#msgs = Message.query.filter_by(receiver=session['id']).all()[-1:]
	msgs = Message.query.order_by(Message.id.desc()).first()
	engine.say(msgs.msg)
	engine.runAndWait()


@app.route('/listen',methods=['GET','POST'])
def listen():
	global allow_speak
	new_msg = voice_rec()
	new_msg_obj= Message(msg=new_msg,sender=session['id'],receiver=0,user=session['id'])
	db.session.add(new_msg_obj)
	db.session.commit()
	bot_msg=''
	if 'time' in new_msg or 'date' in new_msg:
		bot_msg=str(now.hour) +":"+str(now.minute)
	else:
		bot_msg=str(chat(new_msg))
		if check_str(bot_msg) != 'nu':
			return redirect(check_str(bot_msg))
	allow_speak =True
	new_msg_obj= Message(msg=bot_msg,sender=0,receiver=session['id'],user=session['id'])
	db.session.add(new_msg_obj)
	db.session.commit()
	#speak() 
	return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    #bot-chat function
	global allow_speak
	if session.get('logged_in'):
	   if allow_speak == True:
		   speak() 
		   allow_speak =False
	   #if request.method == 'POST' :
		   #print(voice_rec())

	   if request.method == 'POST':
		   new_msg = request.form.get('message')
		   
		   
		   print(new_msg)
		   new_msg_obj= Message(msg=new_msg,sender=session['id'],receiver=0,user=session['id'])
		   db.session.add(new_msg_obj)
		   db.session.commit()
		   if 'time' in new_msg or 'date' in new_msg:
			   bot_msg = str(now.hour) +":"+ str(now.minute)
		   else:
			   bot_msg=str(chat(new_msg))
			   if check_str(bot_msg) != 'nu':
				   return redirect(check_str(bot_msg))
		   allow_speak = True

           #####
		   new_msg_obj= Message(msg=bot_msg,sender=0,receiver=session['id'],user=session['id'])
		   db.session.add(new_msg_obj)
		   db.session.commit()
		   #Messages.query.filter_by(sender=session['id'])
		   return redirect('/#')   
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		return render_template('index.html',msgs=Message.query.filter_by(user=session['id']).all()[-5:], func=speak)
	return render_template('index.html',msgs=Message.query.filter_by(user=session['id']).all()[-5:], func=speak)



@app.route('/login',methods=['POST','GET'])
def login():
    #Login Form
	if request.method == 'GET':
		return render_template('authentication-login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User_table.query.filter_by(username=name, password=passw).first()
			if data is not None :
				session['logged_in'] = True
				session['id'] = data.id
				return redirect(url_for('home'))
			else:
				return 'Wrong credentials'
		except:
			return "Wrong credentials"

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect(url_for('home'))  

@app.route('/register',methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		new_user = User_table(username=request.form['username'], password=request.form['password'], name=request.form['name'], iban='', money='', debts='', weight='', height='',age='')
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('authentication-register.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/traffic')
def traffic():
	return render_template('traffic.html')

@app.route('/health')
def health():
	return render_template('health.html')

@app.route('/office')
def office():
	return render_template('office.html')

@app.route('/calendar')
def calendar():
	return render_template('calendar.html')

@app.route('/weather')
def weather():
	return render_template('weather.html')

@app.route('/bank')
def bank():
	return render_template('bank.html')


if __name__ == '__main__':
    db.create_all()
    app.secret_key = '123'