from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    """
    This function Load posts from the JSON file.
    """
    try:
        with open('blog_posts.json', 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """
    This function saves posts to the JSON file.
    """
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


# CRUD Operations
def add_post(author, title, content):
    """
    This function is responsible for adding the new blog post to the list of posts
    (and saving it to the JSON file).
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


def delete_post(post_id):
    """
    This function handles removing the post from the JSON file.
    """
    posts = load_posts()
    updated_posts = []  # to store the posts that we want to keep.
    for post in posts:
        # This is a condition that filters the posts.
        # It means "include this post in the new list only if the id of the post is not equal to post_id".
        if post['id'] != post_id:
            updated_posts.append(post)
    save_posts(updated_posts)
# or can be written like this:     posts = [post for post in posts if post['id'] != post_id]


def fetch_post(post_id):
    """
    This function looks through the existing posts and returns the post with that ID.
    """
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """
    This function handles the root route of the web application.
    It loads the list of blog posts from the JSON file and renders the 'index.html' template,
    passing the list of posts to it.

    Returns:
        str: The rendered HTML content for the home page.
    """
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    This function supports both GET and POST requests.
    If the request method is GET, it renders the 'add.html' template to display the form
    for creating a new blog post. If the request method is POST, it processes the form data,
    creates a new blog post, saves it to the JSON file, and then redirects the user to the home page.

    Returns:
        str: The rendered HTML content for the add page (for GET requests), or a redirect to the home page
        (for POST requests).
    """
    if request.method == 'POST':
        # The request.form object is a dictionary that contains the form data.
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Validate that none of the fields are empty after stripping whitespace
        if not author or not title or not content:
            return "all fields must be filled properly", 400

        # If validation passes, add the new post
        add_post(author, title, content)
        return redirect(url_for('index'))
        # After the new post is added, this line redirects the user to the index page (/).
        # The redirect function is used to send the user to a different URL,
        # and url_for('index') generates the URL for the index function (which shows the list of all blog posts).
    return render_template('add.html')
    # If request method is not POST (which means it's a GET request, the default method when you visit a webpage),
    # this line renders the add.html template.
    # Rendering a template means creating an HTML page based on the template and sending it to the user's browser.


@app.route('/delete/<int:post_id>', methods=['POST'])   # tells Flask that post_id should be treated as an int.
def delete(post_id):
    """
    This function deletes a blog post with the specified ID. It is only accessible via a POST request.
    """
    delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    This function supports both GET and POST requests. If the request method is GET,
    it renders the 'update.html' template, pre-populated with the current details of the blog post to be updated.
    If the request method is POST, it processes the form data, updates the specified blog post,
    saves the changes to the JSON file, and then redirects the user to the home page.
    """
    post = fetch_post(post_id)
    if post is None:    # If no post with the specified post_id is found, post will be None
        return "Post is not found, *sad face*", 404
        # This is important for handling cases where a user might try to update a non-existent post.

    # This condition ensures that the following code only runs when the form is submitted
    # (not when the page is first loaded, which would be a GET request).
    if request.method == 'POST':
        # request.form: This is dictionary-like object in Flask that contains all the data submitted via the form.
        # These lines extract the updated values that the user has entered into the form fields for
        # author, title, and content.
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        # After calling load_posts(), posts will contain a list of dictionaries,
        # where each dictionary represents a blog post.
        posts = load_posts()
        for post in posts:
            if post['id'] == post_id:
                # If the current post has the matching ID, update its author field with the new value from the form.
                post['author'] = author
                post['title'] = title   # Similarly, update the title field.
                post['content'] = content   # and update the content field.
                break
                # There’s no need to continue looping through the other posts
                # because the correct post has already been found and updated.
        save_posts(posts)
        return redirect(url_for('index'))

    else:   # If request is not a POST request (i.e. it’s a GET request), this line renders update.html template.
        return render_template('update.html', post=post)    # and passes the post object to it.


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
