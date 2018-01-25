from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from app import db, app
from model import Blog, User
import re

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

@app.route('/')
def index():
    users=User.query.all()    
    return render_template('index.html', users=users)

@app.route('/addblog', methods=['POST', 'GET'])
def addblog():
    if request.method=='POST':
        error=''  
        owner=User.query.filter_by(username=session['username']).first()        
        name = request.form['name']
        content = request.form['content']
        if not name or not content:
            error='     -------Please fill the the name and the content of the blog'
            return render_template('addblog.html',error=error)
        new_blog = Blog(name, content, owner)
        db.session.add(new_blog)
        db.session.commit()
        user_blogs=Blog.query.filter_by(owner_id=new_blog.owner_id).all()
        username=User.query.filter_by(id=new_blog.owner_id).first()
        return render_template('blog.html', user_blogs=user_blogs, username=username)
        
    return render_template('addblog.html')

@app.route('/allblog')
def allblog():
    users=User.query.all()
    blogs=Blog.query.all()

    return render_template('allblog.html', users=users, blogs=blogs)

@app.route('/blog/<string:id>/', methods=['POST', 'GET'])
def blog(id):  
    user_blogs=Blog.query.filter_by(owner_id=id).all() 
    username=User.query.filter_by(id=id).first()   

    return render_template('blog.html', user_blogs=user_blogs, username=username)

@app.route('/signup', methods=['POST', 'Get'])
def signup():
    if request.method=='POST':
        error_name=''
        error_password=''       
        username = request.form['username']
        password_top = request.form['password_top']
        password_bot = request.form['password_bot']        
        
        uname=re.compile('\S{3,20}$')
        unamecheck=uname.match(username)
        
        if not unamecheck:
            error_name='Please enter an username between 3 and 20 characters and no spaces.'

        if password_bot!=password_top:
            error_password='Passwords do not match'
        else:
            password=re.compile('\S{3,20}$')
            password_check=password.match(password_top)
            if not password_check:
                error_password='Please enter a password between 3 and 20 characteres and no spaces.'      
                       
        
        if  error_password or error_name:
            return render_template('signup.html',error_name=error_name,
                                   error_password=error_password,                                   
                                   username=username)
        existing_user=User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password_top)
            db.session.add(new_user)
            db.session.commit()
            session['username']=username
            return render_template('addblog.html',
                                    username=username)
        else:
            already_exist='Username already in use, please choose another one.'        
            return render_template('signup.html', already_exist=already_exist)
    else:    
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password==user.password:
            session['username']=username
            return render_template('addblog.html')
        else:
            error='Username and password do not match'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


app.run()