from flask import Flask,render_template,request,redirect, url_for,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#create a secret key to encrypt and decrypt sesion data
app.secret_key="hello"
# to hold session data for a longtime
#app.permanent_session_lifetime=timedelta(days=5)

#configurations for database
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)

#defining the table interms of classess
class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    #Action = db.Column(nullable=True)

   
    def __init__(self,name,email):
        self.email=email
        self.name=name

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/view')
def view():
    values=users.query.all()
    return render_template("view.html",value=values)

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
 #       session.permanent=True
        usr=request.form["nam"]
        session["user"]=usr

        found_user=users.query.filter_by(name=usr).first()
        if found_user:
            session["email"]=found_user.email
        else:
            new_user=users(usr,"")
            db.session.add(new_user)
            db.session.commit()

        flash("Login successfull")
        return redirect(url_for("greeting"))
    else:
        if "user" in session:
            flash("Already logged in ")
            return redirect(url_for("greeting"))
            
    return render_template("login.html")

@app.route('/greet',methods=["POST","GET"])
def greeting():
    email=None
    if "user" in session:
        user=session["user"]
        if request.method == "POST":
            email=request.form["email"]
            session["email"]=email
            found_user=users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("email was saved")
        else:
            if "email" in session:
                email=session["email"]
        return render_template("user.html",email=email)
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    flash("You have been logged out successfully","info")
    session.pop('user',None)
    session.pop('email',None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)