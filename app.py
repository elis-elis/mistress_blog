from flask import Flask, render_template, request, redirect, url_for
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
    """
    This function is responsible for adding the new blog post to the list of posts (and saving it to the JSON file).
    """
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


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # The request.form object is a dictionary that contains the form data.
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        add_post(author, title, content)
        return redirect(url_for('index'))
        # After the new post is added, this line redirects the user to the index page (/).
        # The redirect function is used to send the user to a different URL,
        # and url_for('index') generates the URL for the index function (which shows the list of all blog posts).
    return render_template('add.html')
    # If the request method is not POST (which means it's a GET request, the default method when you visit a webpage),
    # this line renders the add.html template.
    # Rendering a template means creating an HTML page based on the template and sending it to the user's browser.


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
