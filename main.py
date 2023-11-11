from flask import Flask, url_for, render_template, request, redirect, flash, session
from utils.database_scripts import insert_query_user, find_user_login, get_all_cities, log_user_session, update_user_new_login, select_all_from_table, get_all_states
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
    locations = get_all_cities()
    return render_template('index.html', msg='', login=url_for("login"), locations=locations)

def get_locationdata(selected_state, locationcat):
    where_clause = "state = '" + selected_state + "' and locationcategory ='" + locationcat + "'"
    data = select_all_from_table('location', where_clause)
    card_data = []
    for i, each in enumerate(data):
        location = {}
        location['title'] = each[1]
        location['name'] = each[2]
        location['description'] = each[3]
        location['image'] = each[5]
        location['class'] = each[1] + str(i)
        card_data.append(location)
    return card_data  
    
def get_locationdata_new(selected_state):
    where_clause = "city = '" + selected_state + "'"
    data = select_all_from_table('city_places', where_clause)
    card_data = []
    for i, each in enumerate(data):
        location_details = {}
        location_details['title'] = selected_state
        location_details['name'] = each[2]
        location_details['description'] = each[5]
        location_details['image'] = "https://im.hunt.in/cg/Vijayawada/City-Guide/xMary-Matha-Shrine.jpg"
        location_details['class'] = each[1] + str(i)
        card_data.append(location_details)
    return card_data  

@app.route('/travelblog/locationnewtest', methods=['GET', 'POST'])
def locationdetails_new():
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    selected_city = request.form.get('selected_state')
    locations = get_all_cities()
    cities = [location['city'] for location in locations] 
    print(locations)
    if selected_city in cities:
        print(selected_city)
        session['state'] = selected_city
    else:
        selected_city = "Agartala"
    #     locationcat = 'beaches' 
    # session['location'] = locationcat
    get_details = get_locationdata_new(selected_city)
    card_data = get_details
    return render_template('location_select.html', username1= username, 
                           city = selected_city,
                           card_data=card_data)
    
@app.route('/travelblog/profile/locationdetails', methods=['GET', 'POST'])
def locationdetails():
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    selected_state = request.form.get('textfrombox')
    locations = get_all_states() 
    if selected_state in locations:
        print(locations)
        session['state'] = selected_state
    else:
        selected_state = "Karnataka"
        locationcat = 'beaches' 
    session['location'] = locationcat
    get_details = get_locationdata(selected_state, locationcat)
    card_data = get_details
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
        password_db = ""
        try:
            password_db = find_user_login(username)
        except IndexError as e:    
            error = 'Invalid User! Please Register' 
        if password_db != "" and password_db.strip() != password.strip():
            print("after validation", password_db)
            error = 'Invalid User Credentials! Please try Again'
        elif password_db == "" :
            print("check none", password_db)
            redirect(url_for("register"))
        else:
            print(password_db)
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


@app.route('/travelblog/forgotpassword')
def reset_password():
    locations = get_all_cities()
    print(locations)
    return render_template('forgotpassword.html')
    
    
@app.route('/travelblog/profile/<username>')
def profile(username):
    locations = get_all_cities()
    print(locations)
    return render_template('profile.html', username1=username, locations=locations)
    

@app.route('/travelblog/logout')
def logout():
    if 'username' in session: 
        username = session['username']
        session_id = str(session.sid)
        session.pop('username', None)
        session.pop('sid', None)
        log_user_session(username, session_id)
    locations = get_all_states()
    return render_template('index.html', msg='', login=url_for("login"), locations=locations)


if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
    app.run(debug=True)
