import mistune

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required, current_user
from werkzeug.security import check_password_hash

from blog import app
from .database import session
from .models import Post, User

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
  # Zero-Indexed page
  page_index = page -1
  
  count = session.query(Post).count()
  
  start = page_index * paginate_by
  end = start + paginate_by
  
  total_pages = (count - 1) / paginate_by + 1
  has_next = page_index < total_pages - 1
  has_prev = page_index > 0
  
  posts = session.query(Post)
  posts = posts.order_by(Post.datetime.desc())
  posts = posts[start:end]
  
  return render_template(
    "posts.html", 
    posts=posts,
    has_next=has_next,
    has_prev=has_prev,
    page=page,
    total_pages=total_pages
  )
  
# @app.route("/post/add", methods=["GET"])
# def add_post_get():
#   return render_template("add_post.html")
  
# @app.route("/post/add", methods=["POST"])
# def add_post_post():
#   post = Post(
#     title=request.form["title"],
#     content=mistune.markdown(request.form["content"])
#   )
#   session.add(post)
#   session.commit()
#   return redirect(url_for("posts"))
  
@app.route("/post/add", methods=["GET", "POST"])
@login_required
def add_post():
  if request.method == "POST":
    post = Post(
      title=request.form["title"],
      content=request.form["content"],
      author=current_user
    )
    session.add(post)
    session.commit()
    flash("Post added successfully!", "success")
    return redirect(url_for("posts"))
  else:
    return render_template("add_post.html")
  
@app.route("/post/<int:post_id>")
def show_post(post_id):
  post = session.query(Post).get(post_id)
  return render_template("show_post.html", post=post)
  
@app.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
  post = session.query(Post).get(post_id)
  
  # import pdb;
  # pdb.set_trace()
  
  if request.method == "POST":
    post.title=request.form["title"]
    post.content=request.form["content"]
    session.add(post)
    session.commit()
    flash("Post updated successfully!", "success")
    return redirect(url_for("posts"))
  
  return render_template("edit_post.html", post=post)

@app.route("/post/delete/<int:post_id>")
@login_required
def delete_post(post_id):
  # import pdb;
  # pdb.set_trace()
  
  post = session.query(Post).get(post_id)
  # use some sort of JS script to ask if you really want to delete?!
  session.delete(post)
  session.commit()
  flash("Post deleted successfully!", "success")
  # flash("Post was not deleted!")
  
  return redirect(url_for("posts"))
  
# with app.test_request_context():
#   print url_for('posts')
#   print url_for('add_post')
#   print url_for('show_post', post_id=26)
#   print url_for('edit_post', post_id=18)
#   print url_for('delete_post', post_id=6)

@app.route("/login", methods=["GET"])
def login_get():
  return render_template("login.html")
  
@app.route("/login", methods=["POST"])
def login_post():
  email = request.form["email"]
  password = request.form["password"]
  user = session.query(User).filter_by(email=email).first()
  if not user or not check_password_hash(user.password, password):
    flash("Incorrect username or password", "danger")
    return redirect(url_for("login_get"))
  login_user(user)
  return redirect(request.args.get('next') or url_for("posts"))
    