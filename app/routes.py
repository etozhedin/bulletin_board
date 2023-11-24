from flask import Flask, jsonify, request
from . import app, db
from . import app
from .models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    return jsonify({"message": "User registered"}), 201