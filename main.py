from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only

app= Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:asd@localhost:8887/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
app.secret_key = 'asd'
db=SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(120))

    def __init__(self, name, content):
        self.name = name
        self.content = content

@app.route('/')
def index():
    blogs=Blog.query.all()
    
    return render_template('index.html', blogs=blogs)

@app.route('/addblog')
def addblog():
    return render_template('addblog.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method=='POST':
        name = request.form['name']
        content = request.form['content']
        new_blog = Blog(name, content)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('blog.html', name=name, content=content)

    else:
        name = request.args.get('name')
        content = request.args.get('content')

        return render_template('blog.html', name=name, content=content)


app.run()