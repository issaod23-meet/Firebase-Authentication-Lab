from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyAn9QXGBLMiHCx0UxrdioPlVZfIZ_-0VeY",
  "authDomain": "fir-lab-a90ac.firebaseapp.com",
  "projectId": "fir-lab-a90ac",
  "storageBucket": "fir-lab-a90ac.appspot.com",
  "messagingSenderId": "812510174445",
  "appId": "1:812510174445:web:88c69b0d7739ce5bb2c0e4",
  "measurementId": "G-FXS9YMVBBG","databaseURL":""
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return render_template("add_tweet.html")
    except:
           error = "Authentication failed"
           return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return render_template("add_tweet.html")
    except:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)