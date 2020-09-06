from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


app = Flask(__name__)
app.config['FLASK_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(48), nullable=False, default='N/A')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)


all_post = [
    {
        'title': 'Intial Post',
        'content': 'The flask script is nice to start a local development server, but you would have to restart it manually after each change to your code. That is not very nice and Flask can do better. If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong. You can also control debug mode separately from the environment by exporting FLASK_DEBUG=1..',
        'Author': 'Gideon Nimoh'
    },
    {
        'title': 'Subsequent Post',
        'content': 'The flask script is nice to start a local development server, but you would have to restart it manually after each change to your code. That is not very nice and Flask can do better. If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong. You can also control debug mode separately from the environment by exporting FLASK_DEBUG=1..'
    },
     {
        'title': 'Another Post',
        'content': 'The flask script is nice to start a local development server, but you would have to restart it manually after each change to your code. That is not very nice and Flask can do better. If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong. You can also control debug mode separately from the environment by exporting FLASK_DEBUG=1..'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post.html', posts=all_post)

@app.route('/get', methods = ['POST'])
def get():
    return "<h1>You get this web only<h1>"

if __name__ == "__main__":
    app.run(debug=True)