from flask import Flask, jsonify, request
from . import app, db
from . import app
from .models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    post_list = [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
    return jsonify(post_list)

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({"id": post.id, "title": post.title, "content": post.content})

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Optionally, return a forbidden error
        return jsonify({'error': 'You do not have permission to delete this post'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post has been deleted'}), 200



@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    new_post = Post(title=data['title'], content=data['content'], author=current_user)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created.", "post": {"id": new_post.id, "title": new_post.title, "content": new_post.content}}), 201

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    password_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=password_hash)
    print(data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201


@app.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # Assuming passwords are hashed
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "pong"}), 200