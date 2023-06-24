import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'app.log'
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Retrieve all posts from the database
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()

    conn.close()

    # Display the posts on the webpage
    html = '<h1>Posts</h1>'
    for post in posts:
        html += f'<h2>{post[1]}</h2>'
        html += f'<p>{post[2]}</p>'

    return html


@app.route('/post/<int:post_id>')
def get_post(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Retrieve the post from the database
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()

    conn.close()

    if post:
        logger.info(f'Accessed post with ID: {post_id} - Title: {post[1]}')
        html = f'<h1>{post[1]}</h1>'
        html += f'<p>{post[2]}</p>'
        return html
    else:
        logger.warning(f'404 - Post not found with ID: {post_id}')
        return 'Post not found', 404


@app.route('/about')
def about():
    logger.info('Accessed the "About Us" page')
    return '<h1>About Us</h1><p>Welcome to our website!</p>'


@app.route('/healthz')
def health_check():
    response = {'result': 'OK - healthy'}
    return jsonify(response), 200


@app.route('/metrics')
def get_metrics():
    connection_count = 0
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Retrieve post count
    c.execute('SELECT COUNT(*) FROM posts')
    post_count = c.fetchone()[0]

    # Get database connection count
    connection_count += 1

    conn.close()

    response = {
        'post_count': post_count,
        'db_connection_count': connection_count
    }

    return jsonify(response), 200


@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Insert the new post into the database
        c.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()

        conn.close()

        logger.info(f'Created a new post: {title}')

        return 'Post created successfully', 200

    return render_template('create_post.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3111')
