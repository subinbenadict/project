from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL Database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123", # Adjust to your MySQL password
    database="login_db", # Ensure this database exists
    port=3306
)
cursor = connection.cursor(buffered=True)

# ----------------------------------------------------
# AUTHENTICATION ROUTES (Login & Signup)
# ----------------------------------------------------

@app.route('/')
def index():
    # Automatically direct users to the login page when they open the app
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        insert_query = """
        INSERT INTO users (username, email, phone, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, email, phone, password))
        connection.commit()
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Login successful, go to Home
            return redirect(url_for('home', username=user[0]))
        else:
            error_message = "Invalid Username or Password. Please try again."

    return render_template('login.html', error=error_message)


# ----------------------------------------------------
# MAIN WEBSITE ROUTES (The 5 Pages)
# ----------------------------------------------------

@app.route('/home')
def home():
    username = request.args.get('username', 'Guest')
    return render_template('home.html', username=username)

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # If the user submits the contact form
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Ensure you have a 'messages' table in your database for this to work
        insert_query = """
        INSERT INTO messages (name, email, subject, message)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, email, subject, message))
        connection.commit()
        
        # Reload the page or show a success message
        return render_template('contact.html', success="Your message was sent safely!")

    # If the user just clicks the link to view the page
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)