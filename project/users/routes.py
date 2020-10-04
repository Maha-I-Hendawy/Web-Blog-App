from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from .forms import *
from project.models import *
from project import bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from project import images
from flask_mail import Message

mod = Blueprint('users', __name__, template_folder='templates')



@mod.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('site.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash('Your Account Has Been Created', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/register.html', title='Registration Form', form=form)


@mod.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('site.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('site.home'))
		else:
			flash('Login Unsuccessful. Please Check Your Email and Password', 'danger')

	return render_template('users/login.html', title='Login Form', form=form)




@mod.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('site.home'))



@mod.route('/user/<int:user_id>')
def one_user(user_id):
	user = User.query.get_or_404(user_id)

	return render_template('users/user.html', user=user)



@mod.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		if form.picture.data:
			filename = images.save(form.picture.data)
		flash('Your Account Has Been Created', 'success')
		return redirect(url_for('users.update_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('users/update_profile.html', form=form)



def sent_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
	{url_for('users.reset_password', token=token, _external=True)}
	'''
	mail.send(msg)


@mod.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('site.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		sent_reset_email(user)
		flash('An email has been sent to you', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/reset_request.html', title='Request Resset', form=form)




@mod.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('site.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('This is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated. You can login now', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/reset_password.html', title='Reset Password', form=form)
