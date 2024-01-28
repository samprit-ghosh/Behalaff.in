import secrets
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '0df660dd7e2503a4'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resultsDatabase.db'
app.config['SECRET_KEY'] = 'saredevelopersbhaihai404'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

dt = datetime.now()
currentday = dt.strftime('%d/%m/%Y')

lastday = (dt - timedelta(1)).strftime('%d/%m/%Y')
secondlastday = (dt - timedelta(2)).strftime('%d/%m/%Y')
print(currentday)
print(lastday)
print(secondlastday)

now = datetime.now()
print(now)

# 9:55
# 11:25
# 12:55
# 2:25
# 3:55
# 5:25
# 6:55
# 8:25

slots_show = {
    'slot1' : now.replace(hour=9, minute=55, second=0, microsecond=0),
    'slot2' : now.replace(hour=11, minute=25, second=0, microsecond=0),
    'slot3' : now.replace(hour=12, minute=55, second=0, microsecond=0),
    'slot4' : now.replace(hour=14, minute=25, second=0, microsecond=0),
    'slot5' : now.replace(hour=15, minute=55, second=0, microsecond=0),
    'slot6' : now.replace(hour=17, minute=25, second=0, microsecond=0),
    'slot7' : now.replace(hour=18, minute=55, second=0, microsecond=0),
    'slot8' : now.replace(hour=20, minute=25, second=0, microsecond=0),
}

slots_add = {
    'slot1' : now.replace(hour=10, minute=0, second=0, microsecond=0),
    'slot2' : now.replace(hour=11, minute=30, second=0, microsecond=0),
    'slot3' : now.replace(hour=13, minute=0, second=0, microsecond=0),
    'slot4' : now.replace(hour=14, minute=30, second=0, microsecond=0),
    'slot5' : now.replace(hour=16, minute=0, second=0, microsecond=0),
    'slot6' : now.replace(hour=17, minute=30, second=0, microsecond=0),
    'slot7' : now.replace(hour=19, minute=0, second=0, microsecond=0),
    'slot8' : now.replace(hour=20, minute=30, second=0, microsecond=0),
}
# print(now < today8am)
print(now < slots_show['slot1'])

class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    slot_1_1 = db.Column(db.Integer, nullable=True)
    slot_1_3 = db.Column(db.Integer, nullable=True)
    slot_2_1 = db.Column(db.Integer, nullable=True)
    slot_2_3 = db.Column(db.Integer, nullable=True)
    slot_3_1 = db.Column(db.Integer, nullable=True)
    slot_3_3 = db.Column(db.Integer, nullable=True)
    slot_4_1 = db.Column(db.Integer, nullable=True)
    slot_4_3 = db.Column(db.Integer, nullable=True)
    slot_5_1 = db.Column(db.Integer, nullable=True)
    slot_5_3 = db.Column(db.Integer, nullable=True)
    slot_6_1 = db.Column(db.Integer, nullable=True)
    slot_6_3 = db.Column(db.Integer, nullable=True)
    slot_7_1 = db.Column(db.Integer, nullable=True)
    slot_7_3 = db.Column(db.Integer, nullable=True)
    slot_8_1 = db.Column(db.Integer, nullable=True)
    slot_8_3 = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(12), nullable=False)


ADMIN = {'admin': {'password': 'admin@123'}}

@app.route("/")
def home():

    today = Result.query.filter_by(date=currentday).first()
    yesterday1 = Result.query.filter_by(date=lastday).first()
    yesterday2 = Result.query.filter_by(date=secondlastday).first()
    return render_template('index.html', slots_show=slots_show, now=now, today=today, yesterday1=yesterday1, yesterday2=yesterday2)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
    
@app.route("/tips")
def tips():
    return render_template("Tips.html")


    
@app.route("/tipstommorow")
def tipstommorow():
        return render_template("tips-tommorow.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/patti-chart')
def pattichart():
    return render_template("patti-chart.html")


@app.route('/luckypatti')
def luckypatti():
    return render_template("lucky-patti.html")

@app.route('/old')
def old():
    return render_template("old.html")

@app.route('/pattitips')
def pattitips():
    return render_template("patti-tips.html")

@app.route("/admin_auth", methods=['GET', 'POST'])
def admin_auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username in ADMIN and password == ADMIN[username]['password']:
            if 'user_id' in session and session['user_id'] != username:
                app.config['SECRET_KEY'] = secrets.token_hex(16)

            session_token = str(uuid.uuid4())
            session['user_id'] = username
            session['session_token'] = session_token
            return redirect('/admin')
        else:
            flash("Invalid username or password.")
            return redirect(url_for('admin_auth')) 
        
    return render_template('login.html')

@app.route("/admin")
def admin():
    if 'user_id' not in session:
        return redirect("/admin_auth")
    
    daily_data = Result.query.filter_by(date=currentday).first()          

    return render_template('admin.html', slots_add=slots_add, now=now, date=currentday, daily_data=daily_data)


@app.route('/update', methods=['POST'])
def update():
    daily_data = Result.query.filter_by(date=currentday).first()

    if not daily_data:
        daily_data = Result(date=currentday)

    slot = request.form['slots']
    value_1 = request.form['one_digit']
    value_3 = request.form['three_digit']
    print(slot, value_1, value_3)

    if slot == '1':
        daily_data.slot_1_1 = value_1
        daily_data.slot_1_3 = value_3
    elif slot == '2':
        daily_data.slot_2_1 = value_1
        daily_data.slot_2_3 = value_3
    elif slot == '3':
        daily_data.slot_3_1 = value_1
        daily_data.slot_3_3 = value_3
    elif slot == '4':
        daily_data.slot_4_1 = value_1
        daily_data.slot_4_3 = value_3
    elif slot == '5':
        daily_data.slot_6_1 = value_1
        daily_data.slot_6_3 = value_3
    elif slot == '6':
        daily_data.slot_6_1 = value_1
        daily_data.slot_6_3 = value_3
    elif slot == '7':
        daily_data.slot_7_1 = value_1
        daily_data.slot_7_3 = value_3
    elif slot == '8':
        daily_data.slot_8_1 = value_1
        daily_data.slot_8_3 = value_3

    db.session.add(daily_data)
    db.session.commit()

    return redirect('/admin')


@app.route('/admin_logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('session_token', None)
        flash("Logout successful")
        return redirect(url_for('admin_auth')) 
    else:
        return redirect("/admin_auth")

if __name__ == '__main__':
    app.run(debug=True)