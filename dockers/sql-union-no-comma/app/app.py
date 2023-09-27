from flask import Flask, request
from sqlalchemy.sql import text
from flask_bcrypt import Bcrypt
import json
from flask import jsonify

#from flask_pydantic import validate

from database import db, Users, Posts
from models import NameModel
from utils import validate_username


app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://demo:pleasesubscribe@127.0.0.1:3306/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db.init_app(app)


@app.route('/')
def index():
    posts = db.session.query(Posts).all()
    post_list = []
    for post in posts:
        post_list.append({'id': post.id, 'title': post.title, 'content': post.body})
    return jsonify(posts=post_list)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = db.session.query(Posts).filter(Posts.id == post_id).first()
    return jsonify(id=post.id, title=post.title, content=post.body)

@app.route('/user/<username>/', methods=['GET'])
@validate_username
def author(username: str, query: dict):
    # Validate the username parameter
    user = db.session.execute(text(f"SELECT * FROM users WHERE username = '{username}'")).first()        
    return json.dumps(user, default=str)

# Create a route to add a new user
@app.route('/user/add/', methods=['POST'])
def add_user():    
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = Users(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()
    return

# Create a route to add a new post
@app.route('/post/add/', methods=['POST'])
def add_post():    
    title = request.form.get('title')
    body = request.form.get('body')
    author_id = request.form.get('author_id')
    post = Posts(title=title, body=body, author_id=author_id)
    db.session.add(post)
    db.session.commit()
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
