from flask import Flask, url_for, render_template, request, redirect, flash, session
from init_db import insert_query_user, find_user_login, log_user_session, update_user_new_login, select_all_from_table, get_all_states
from flask_session import Session
import os

app = Flask(__name__)

PERMANENT_SESSION_LIFETIME = 10
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True 
app.config['SESSION_REFRESH_EACH_REQUEST'] = True 
app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)


@app.route('/')
def home():
    return redirect(url_for("site_home"))

@app.route('/travelblog/home')
def site_home():
    locations = get_all_states()
    location_all = []
    for location in locations:
        l = {}
        l['state'] = location
        location_all.append(l)
    print(location_all) 
    return render_template('index.html', msg='', login=url_for("login"), locations=location_all)

def get_locationdata(selected_state, locationcat):
    where_clause = "state = '" + selected_state + "' and locationcategory ='" + locationcat + "'"
    data = select_all_from_table('location', where_clause)
    
    card_data = []
    locations = []
    for i, each in enumerate(data):
        location = {}
        location['title'] = each[1]
        location['name'] = each[2]
        location['description'] = each[3]
        location['image'] = each[5]
        location['class'] = each[1] + str(i)
        locations.append(each[1]) 
        card_data.append(location)
    
    return card_data,locations  
    


@app.route('/travelblog/locationdetails', methods=['GET', 'POST'])
def locationdetails():
    username = "ruchi"
    selected_state = request.form.get('selected_state')
    session['state'] = selected_state
    locationcat = 'beaches' 
    session['location'] = locationcat
    get_details = get_locationdata(selected_state, locationcat)
    card_data = get_details[0]
    return render_template('location_select.html', username1= username, 
                           state = selected_state, 
                           locationcat = locationcat,
                           card_data=card_data)

@app.route('/login')
def site_login():
    return redirect(url_for("login"))

@app.route('/travelblog/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        password_db = find_user_login(username)
        if password_db.strip() != password.strip():
            error = 'Invalid User Credentials! Please try Again'
            redirect(url_for("register"))
        else:
            update_user_new_login(username)
            return redirect(url_for("profile", username=username))
        
    return render_template('login.html', msg=error)


@app.route('/travelblog/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form['email']
        try:
            password_db = find_user_login(username)
        except Exception:
            password_db = None
            insert_query_user(username=username, email=email, password=password, fname=fname, lname=lname)
        if not password_db:
            return redirect(url_for("profile", username=username))
        else:
            error = 'user already exists! please try to login!'
            return render_template('login.html', msg=error)
    elif request.method == 'post':
        error = 'please fill out the form!'
    return render_template('register.html', msg=error)


@app.route('/travelblog/profile/<username>')
def profile(username):
    locations = get_all_states()
    return render_template('profile.html', username1=username, locations=locations)
    

@app.route('/travelblog/logout')
def logout():
    # print(session)
    # username = session['username']
    # session_id = str(session.sid)
    # session.pop('username', None)
    # session.pop('sid', None)
    # log_user_session(username, session_id)
    locations = get_all_states()
    return render_template('login.html', msg="", locations=locations)


if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
    app.run(debug=True)
