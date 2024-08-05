from flask import Flask, render_template
import json

app = Flask(__name__)


def load_posts():
    # Load posts from the JSON file
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    # Save posts to the JSON file
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


# CRUD Operations
def add_post(author, title, content):
    posts = load_posts()  # Load the current list of posts from the JSON file
    if not posts:
        new_id = 1
    else:
        new_id = posts[-1]['id'] + 1
        # If there are existing posts, it assigns new_id to be the ID of the last post in the list plus 1.
        # This ensures each new post gets a unique ID that increments from the last post's ID.
    new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
    posts.append(new_post)  # Add the new post to the list of posts
    save_posts(posts)  # Save the updated list of posts back to the JSON file


@app.route('/')
def index():  # sends the list of blog posts to a template for display
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


@app.route('/add-post')
def add_post():
    pass


if __name__ == '__main__':
    app.run()
