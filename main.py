# ---------------------------- IMPORTED MODULES------------------------------- #
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from functools import wraps

# ---------------------------- APPS CONFIG------------------------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# ---------------------------- DB TABLES CONFIGS------------------------------- #
class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(100))

	# This will act like a List of BlogPost objects attached to each User.
	# The "author" refers to the author property in the BlogPost class.
	posts = relationship("BlogPost", back_populates="author")
	comments = relationship("Comments", back_populates="comment_author")


class BlogPost(db.Model):
	__tablename__ = "blog_posts"
	id = db.Column(db.Integer, primary_key=True)

	# Create Foreign Key, "users.id" the users refers to the tablename of User.
	author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	# Create reference to the User object, the "posts" refers to the posts property in the User class.
	author = relationship("User", back_populates="posts")

	title = db.Column(db.String(250), unique=True, nullable=False)
	subtitle = db.Column(db.String(250), nullable=False)
	date = db.Column(db.String(250), nullable=False)
	body = db.Column(db.Text, nullable=False)
	img_url = db.Column(db.String(250), nullable=False)
	comments = relationship("Comments", back_populates="post")


class Comments(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	comment_author = relationship("User", back_populates="comments")
	post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
	post = relationship("BlogPost", back_populates="comments")
	text = db.Column(db.Text, nullable=False)


db.create_all()


# ---------------------------- WRAPPERS & PREEXISTED FUNCTIONS------------------------------- #
def admin_only(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.id != 1:
			return abort(403)
		return f(*args, **kwargs)

	return decorated_function


# ---------------------------- APPS ROUTING & HANDLERS------------------------------- #
@app.route('/')
def get_all_posts():
	posts = BlogPost.query.all()
	return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
	register_form = RegisterForm()
	if register_form.validate_on_submit():
		new_user = User()
		new_user.email = request.form.get("email")
		new_user.password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
		new_user.name = request.form.get("name")
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
		return redirect(url_for("get_all_posts"))
	return render_template("register.html", form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
	logged = LoginForm()
	if logged.validate_on_submit():
		email = logged.email.data
		password = logged.password.data
		user = User.query.filter_by(email=email).first()
		if check_password_hash(user.password, password):
			login_user(user)
			return redirect(url_for('get_all_posts'))
		elif user.password == password:
			login_user(user)
			return redirect(url_for('get_all_posts'))
		else:
			flash("Try again please")
			return redirect(url_for("login"))
	return render_template("login.html", form=logged)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
	requested_post = BlogPost.query.get(post_id)
	comment_form = CommentForm()
	all_comments = Comments.query.all()
	if comment_form.validate_on_submit():
		new_comment = Comments(
			text=comment_form.comment.data,
			comment_author=current_user,
			post=requested_post
		)
		db.session.add(new_comment)
		db.session.commit()
	return render_template("post.html", post=requested_post, comments=all_comments, comment_form=comment_form)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact")
def contact():
	return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
	form = CreatePostForm()
	if form.validate_on_submit():
		new_post = BlogPost(
			title=form.title.data,
			subtitle=form.subtitle.data,
			body=form.body.data,
			img_url=form.img_url.data,
			author=current_user,
			date=date.today().strftime("%B %d, %Y")
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("get_all_posts"))
	return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@login_required
@admin_only
def edit_post(post_id):
	post = BlogPost.query.get(post_id)
	edit_form = CreatePostForm(
		title=post.title,
		subtitle=post.subtitle,
		img_url=post.img_url,
		author=post.author,
		body=post.body
	)
	if edit_form.validate_on_submit():
		post.title = edit_form.title.data
		post.subtitle = edit_form.subtitle.data
		post.img_url = edit_form.img_url.data
		post.author = edit_form.author.data
		post.body = edit_form.body.data
		db.session.commit()
		return redirect(url_for("show_post", post_id=post.id))

	return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
	post_to_delete = BlogPost.query.get(post_id)
	db.session.delete(post_to_delete)
	db.session.commit()
	return redirect(url_for('get_all_posts'))


if __name__ == '__main__':
	app.debug = True
	app.run()
