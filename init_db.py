import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create the posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL)''')

    # Insert sample posts
    sample_posts = [
        ('First Post', 'This is the content of the first post.'),
        ('Second Post', 'This is the content of the second post.'),
        ('Third Post', 'This is the content of the third post.')
    ]
    c.executemany('INSERT INTO posts (title, content) VALUES (?, ?)', sample_posts)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
