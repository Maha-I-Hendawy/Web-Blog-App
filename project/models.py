from datetime import datetime
from project import db, ma, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=True)


	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token():
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.password}')"




class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	content = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref='posts', lazy=True)


	def __repr__(self):
		return f"Post('{self.title}', '{self.content}', '{self.user}')"




class UserSchema(ma.Schema):
	class Meta:
		model = User







class PostSchema(ma.Schema):
	class Meta:
		model = Post





user_schema = UserSchema()
users_schema = UserSchema(many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)