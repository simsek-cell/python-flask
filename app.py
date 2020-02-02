from flask import Flask,redirect,url_for,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy,sqlalchemy
from werkzeug.security import generate_password_hash
import string,random,sendmail

puncchars=[]
for i in string.punctuation:
    puncchars.append(i)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////Users/acer/Flask App/users.db'
app.config["SECRET_KEY"] = "\xba\xcf$bh>q\xa7\xa0\xf1_\xac\x85P0\xd6@X\xbe\x04\x08\xbd`\x80"
db = SQLAlchemy(app)

def issmall(*args):
    for i in args:
        if len(i)<4:
            return True
        else:
            pass

def ispossible(x):
    for i in x:
        if i in puncchars:
            return False
        else:
            return True

class User(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(16),nullable = False , unique = True)
    Password = db.Column(db.String,nullable = False)
    Email = db.Column(db.String(40),nullable=False,unique=True)

@app.route("/")
def homepage(message=None):
    return render_template("home.html",mesaj="Kayıt Başarılı")

@app.route("/registercontrol",methods=["POST"])
def createaccount():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        global email
        email = request.form.get("email")
        if (not issmall(username,password,email)) and ispossible(username):
            global newuser
            newuser = User(Username=username,Password=generate_password_hash(password),Email=email)
            message="Az kaldı."
            flash([message,email])
            return redirect(url_for("emailcontrol"))
        else:
            flash("Kullanıcı adınız veya parolanız 4-16 karakter arasında olmalı ve hatalı karakter içermemelidir.")
            return redirect(url_for("homepage"))
    except:
        hata = "Kullanıcı adınız veya emailiniz, başka bir kullanıcı tarafından kullanılıyor."
        flash(hata)
        return redirect(url_for("homepage"))
        
@app.route("/email")
def emailcontrol():
    global number
    number = random.randrange(1000,9999)
    code = f"""
    <font color='purple' style='font-weight: bold;'>{str(number)}</font>
    """
    sendmail.sendmessage("***@gmail.com","d***",email,code)
    return render_template("emailcontrol.html")

@app.route("/codecontrol",methods=["POST"])
def codecontrol():
    usernumber = int(request.form.get("code"))
    if number == usernumber:
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug = True)
