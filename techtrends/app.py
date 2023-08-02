import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from werkzeug.serving import WSGIRequestHandler


# Configure logger for Werkzeug (Web Server Gateway Interface)
werkzeug_logger = logging.getLogger('werkzeug')
wlogFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
whandler = logging.StreamHandler(sys.stdout)
whandler.setFormatter(wlogFormatter)
werkzeug_logger.addHandler(whandler)
werkzeug_logger.setLevel(logging.DEBUG)

# Configure logger for app  
app_logger = logging.getLogger('app')
alogFormatter = logging.Formatter("%(levelname)s:%(name)s:%(asctime)s, %(message)s'","%m/%d/%Y, %H:%M:%S")
ahandler = logging.StreamHandler(sys.stdout)
ahandler.setFormatter(alogFormatter)
app_logger.addHandler(ahandler)


app_logger.setLevel(logging.DEBUG)





# global Varible for counting DB connections
count_db_connections = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global count_db_connections
    count_db_connections  += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error('Post "%s" not found', post_id)
        return render_template('404.html'), 404
    else:
        app.logger.info('Article "%s" retrieved!', post['title'])
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About us page is retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('Article "%s" created!', title)
            return redirect(url_for('index'))

    return render_template('create.html')


# Healthcheck endpoint
@app.route('/healthz')
def status():
    try:   
        # create connection 
        conn= get_db_connection()  
        cursor = conn.cursor()
        # perform integrity check
        cursor.execute('PRAGMA integrity_check')
        result = cursor.fetchone()[0]
        if(result != 'ok') :
            raise Exception("Database Integrity check not ok")

         # Check if the posts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
        if not cursor.fetchone():
            raise Exception("posts table does not exist")


        # Check if the posts table has the attributes and datatypes
        cursor.execute("PRAGMA table_info(posts)")
        columns = [(column[1], column[2]) for column in cursor.fetchall()]
      
        if columns != [
        ("id", "INTEGER"),
        ("created", "TIMESTAMP"),
        ("title", "TEXT"),
        ("content", "TEXT"),
        ]:
            raise Exception("Post table has unexpected attributes or datatypes")
        conn.close()
        
        # Checks have been passed at this point and so assume healthy
        response = app.response_class(
                response=json.dumps({"result":"OK - healthy"}),
                status=200,
                mimetype='application/json'
            )
        app.logger.info('healthz status request -  healthy')
        return response   
            
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"result":"Not healthy - " + str(e)}),
            status=500,
            mimetype='application/json'
            )
        app.logger.info('healthz status request unhealthy')
        return response
    
   
# Metrics endpoint
@app.route('/metrics')
def metrics():

    connection = get_db_connection()
    count = connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    connection.close()

    response = app.response_class(
            response=json.dumps({"db_connection_count":count_db_connections ,"post_count":count}),
            status=200,
            mimetype='application/json'
    )
    return response    


# start the application on port 3111
if __name__ == "__main__":

   app.run(host='0.0.0.0', port='3111')
   



   



