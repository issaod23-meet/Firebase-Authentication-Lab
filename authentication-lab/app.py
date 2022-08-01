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
  "measurementId": "G-FXS9YMVBBG","databaseURL":"https://fir-lab-a90ac-default-rtdb.europe-west1.firebasedatabase.app/",
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        print(login_session)
        return render_template("add_tweet.html")
    except:
           error = "Authentication failed"
           print('GEUWCDJSHK')
           return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       username= request.form['username']
       bio = request.form['bio']
       name = request.form['fullname']
       user = {'name': name, 'bio':bio, 'username': username}
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        db.child('Users').child(login_session['user']['localId']).set(user)

        return render_template("add_tweet.html")
    except:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    print(login_session)
    title = request.form['title']
    tweets= request.form['tweet']
    tweet = {'title': title,'tweet': tweets,"uid":login_session['user']['localId']}
    db.child('tweets').push(tweet)
    return render_template("add_tweet.html")
    db.child('Users').child(login_session['user']['localId']).set(user)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return render_template("signin.html")

@app.route('/all_tweets')
def alltweets():
    x = db.child('tweets').get().val()
    return render_template("tweets.html")



if __name__ == '__main__':
    app.run(debug=True)