from flask import Blueprint, render_template, url_for
from .forms import MessageForm


mod = Blueprint('site', __name__, template_folder='templates')


@mod.route('/')
@mod.route('/home')
def home():
	return render_template('site/home.html')


