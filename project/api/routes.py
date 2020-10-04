from flask import Blueprint, request, jsonify
from project.models import *

mod = Blueprint('api', __name__,)


# Users API

@mod.route('/user', methods=['POST'])
def add_user():
	username = request.json['username']
	email = request.json['email']
	password = request.json['password']

	new_user = User(username=username, email=email, password=password)
	db.session.add(new_user)
	db.session.commit()

	return user_schema.jsonify(new_user)


@mod.route('/user', methods=['GET'])
def all_users():
	users = User.query.all()
	result = users_schema.dump(users)

	return jsonify(result)


@mod.route('/user/<int:id>', methods=['GET'])
def one_user(id):
	user = User.query.get(id)

	return user_schema.jsonify(user)



@mod.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
	user = User.query.get(id)

	username = request.json['username']
	email = request.json['email']
	password = request.json['password']

	user.username = username
	user.email = email
	user.password = password

	db.session.commit()

	return user_schema.jsonify(user)




@mod.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
	user = User.query.get(id)

	db.session.delete(user)
	db.session.commit()

	return user_schema.jsonify(user)



# Posts API 


@mod.route('/post', methods=['POST'])
def add_post():
	title = request.json['title']
	content = request.json['content']
	user_id = request.json['user_id']

	new_post = Post(title=title, content=content, user_id=user_id)
	db.session.add(new_post)
	db.session.commit()


	return post_schema.jsonify(new_post)



@mod.route('/post', methods=['GET'])
def all_post():
	posts = Post.query.all()
	result = posts_schema.dump(posts)

	return jsonify(result)



@mod.route('/post/<int:id>', methods=['GET'])
def one_post(id):
	post = Post.query.get(id)

	return post_schema.jsonify(post)




@mod.route('/post/<int:id>', methods=['PUT'])
def update_post(id):
	post = Post.query.get(id)

	title = request.json['title']
	content = request.json['content']
	user_id = request.json['user_id']

	post.title = title 
	post.content = content 
	post.user_id = user_id 

	db.session.commit()

	return post_schema.jsonify(post)




@mod.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
	post = Post.query.get(id)

	db.session.delete(post)
	db.session.commit()

	return post_schema.jsonify(post)


