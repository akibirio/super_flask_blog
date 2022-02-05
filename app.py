import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort  # for the sake of returning HTTP eror 404 if post not found

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# function called to get details of a single post, together i=with get_posts function above.
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

app.run()