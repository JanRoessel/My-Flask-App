from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

POSTS_FILE = 'posts.json'

def read_posts():
    with open(POSTS_FILE, 'r') as f:
        return json.load(f)

def write_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = read_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = read_posts()
        new_id = max(post['id'] for post in posts) + 1 if posts else 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }
        posts.append(new_post)
        write_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = read_posts()
    posts = [post for post in posts if post['id'] != post_id]
    write_posts(posts)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)