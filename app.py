from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:asd@localhost:8887/blogz'
app.config['SQLALCHEMY_ECHO']=True
app.secret_key = 'asd'
db=SQLAlchemy(app)