from flask import render_template, flash, redirect, url_for,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from app import app, db, lm

from app.models.forms import LoginForm, PostForm,SigninForm
from app.models.tables import User,Post,Follow

@lm.user_loader
def load_user(id):
       return User.query.filter_by(id=id).first()

## Post / Index ##

@app.route("/",methods=["GET","POST"])
def index():
   postform = PostForm()
   post_list = Post.query.order_by(Post.id.desc()).all()
   if current_user.is_authenticated:
         following_post_list = Post.query.join(Follow, Follow.user_id == Post.user_id).filter(Follow.follower_id == current_user.id).order_by(Post.id.desc()).all()
         print(following_post_list)
         my_post_list = Post.query.filter_by(user_id=current_user.id).order_by(Post.id.desc()).all()
         users = User.query.filter(User.id != current_user.id).all()
   else:
         following_post_list = []
         my_post_list = []
         users = User.query.all()
   if postform.validate_on_submit():
          p = Post(postform.text.data,current_user.id)
          db.session.add(p)
          db.session.commit()
          return redirect(url_for("index"))
   return render_template("index.html",
                           postform=postform,
                           post_list=post_list,
                           following_post_list=following_post_list,
                           my_post_list=my_post_list,
                           users=users)

@app.route("/delete-post/<int:id_post>",methods=["GET"])
@login_required
def delete_post(id_post):
      post = Post.query.filter_by(id=id_post).first()
      if post and (current_user.id == post.user_id):
         db.session.delete(post)
         db.session.commit()
         return redirect(url_for("index"))
      else:
         flash("Erro ao deletar post.")

@app.route("/followers/",methods=["GET"])
@login_required
def followers():
      followers = db.session.query(Follow.follower_id).filter_by(user_id=current_user.id).all()
      return jsonify(followers)

@app.route("/follow/<int:id_user>",methods=["GET"])
@login_required
def follow(id_user):
      exists = Follow.query.filter(Follow.user_id == current_user.id,Follow.follower_id == id_user).first()
      if not exists:
         follow = Follow(current_user.id,id_user)
         db.session.add(follow)
         db.session.commit()
         return 'true'

@app.route("/unfollow/<int:id_user>",methods=["GET"])
@login_required
def unfollow(id_user):
      exists = Follow.query.filter(Follow.user_id == current_user.id,Follow.follower_id == id_user).first()
      if exists:
         db.session.delete(exists)
         db.session.commit()
         return 'true'

## End Post / Index ##

##### Login #####

@app.route("/login",methods=["GET","POST"])
def login():
       form = LoginForm()
       if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
               login_user(user)
               return redirect(url_for("index"))
            else:
               flash("Usuário ou senha inválidos.")
       return render_template("login.html",
                              form = form)

@app.route("/signin",methods=["GET","POST"])
def signin():
       form = SigninForm()
       if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(username=form.email.data).first()
            if user and email:
               flash("Usuário ou email já cadastrado.")
            else:
               new_user = User(form.username.data,
                              form.password.data,
                              form.name.data,
                              form.email.data)
               db.session.add(new_user)
               db.session.commit()
               login_user(new_user)    
               return redirect(url_for("index"))
       return render_template("signin.html",
                              form = form)


@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
   logout_user()
   return redirect(url_for("index"))

##### End Login #####