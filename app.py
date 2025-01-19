from flask import Flask, render_template, request, redirect, url_for, session, flash

# use python app.py then open http://127.0.0.1:5000/


app = Flask(__name__)
app.secret_key = '093433ef39d30157d885147353561ad7'  # Secret key for session handling

# Predefined user credentials (for simplicity)
users = {
    "testuser": "password123"  # username: password
}

# Predefined job listings
jobs = [
    {"title": "Software Engineer", "company": "TechCorp", "location": "New York", "email": "hr@techcorp.com"},
    {"title": "Data Analyst", "company": "DataSolutions", "location": "San Francisco", "email": "jobs@datalsolutions.com"},
    {"title": "Web Developer", "company": "Webify", "location": "Remote", "email": "contact@webify.com"}
]

@app.route('/')
def index():
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    if 'user' in session:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    return render_template('landing.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('query', '').lower()
    location_query = request.args.get('location', '').lower()
    filtered_jobs = [job for job in jobs if 
                     (search_query in job['title'].lower() or not search_query) and
                     (location_query in job['location'].lower() or not location_query)]

    return render_template('home.html', jobs=filtered_jobs, user=session.get('user'))

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        email = request.form['email']
        new_job = {"title": title, "company": company, "location": location, "email": email}
        jobs.append(new_job)
        return redirect(url_for('home'))
    return render_template('post_job.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists.")
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
