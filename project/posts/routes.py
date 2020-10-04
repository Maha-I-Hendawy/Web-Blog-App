from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from .forms import *
from flask_login import login_required, current_user
from project.models import *



mod = Blueprint('posts', __name__, template_folder='templates')


@mod.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
	form = PostForm()
	if form.validate_on_submit():
		new_post = Post(title=form.title.data, content=form.content.data, user=current_user)
		db.session.add(new_post)
		db.session.commit()
		flash('Your Post Has Been Created', 'success')
		return redirect(url_for('posts.all_posts'))
	return render_template('posts/create_post.html', title='Create Post', form=form)
	



@mod.route('/all_posts')
def all_posts():
	posts = Post.query.all()

	return render_template('posts/all_posts.html', posts=posts)



@mod.route('/post/<int:post_id>')
def one_post(post_id):
	post = Post.query.get_or_404(post_id)

	return render_template('posts/post.html', post=post)



@mod.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.user != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your Post Has Been Updated', 'success')
		return redirect(url_for('posts.one_post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('posts/create_post.html', title='Update Post', form=form)




@mod.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.user != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your Post Has Been Deleted', 'success')
	return redirect(url_for('site.home'))