from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['FLASK_DEBUG'] = True
app.config['SECRET_KEY'] = "ogidi@12"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(48), nullable=False, default='N/A')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    confirm = db.Column(db.String(80), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def get_id(id):
    return User.query.get(id)

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.username == request.form['username']).first()
        if user and check_password_hash(user.password, password):
            user.authenticated = True
            login_user(user, remember=True)
            flash("You have successfully logged in")
            return redirect(url_for('home'))
        else:
            flash("Please check Username or Password")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        pswd_hash = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        if user or password != confirm:
            flash("Password do not match or Email already in use", "error")
        else:
            new_user = User(name=name, username=username, email=email, password=pswd_hash, confirm=confirm)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("You have successfully registered. Please kindly Login below", "info")
            return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user(user)
    return redirect('/')


@app.route('/home/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post'))
    else:
        all_post = BlogPost.query.order_by(BlogPost.date).all()
        return render_template('post.html', posting=all_post)

@app.route('/home/post/delete/<int:id>')
@login_required
def delete(id):
    posts = BlogPost.query.get_or_404(id)
    db.session.delete(posts)
    db.session.commit()
    return redirect(url_for('post'))


@app.route('/home/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    posts = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        posts.title = request.form['title']
        posts.content = request.form['content']
        posts.author = request.form['author']
        db.session.commit()
        return redirect(url_for('post'))
    else:
        return render_template('edit.html', post=posts)


@app.route('/home/post/new', methods=['GET', 'POST'])
@login_required
def newpost():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post'))
    else:
        return render_template('/newpost.html')

if __name__ == "__main__":
    app.run(debug=True)