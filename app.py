from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

with open('blog_posts.json', 'r', encoding='utf-8') as read_file:
    blog_posts = json.load(read_file)


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        new_post = {
            "id": len(blog_posts) + 1,
            "author": request.form.get('Author'),
            "title": request.form.get('Title'),
            "content": request.form.get('Content')
        }
        blog_posts.append(new_post)

        with open('blog_posts.json', 'w', encoding='utf-8') as write_file:
            json.dump(blog_posts, write_file, indent=2)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    with open('blog_posts.json', 'w', encoding='utf-8') as write_file:
        json.dump(blog_posts, write_file, indent=2)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    def fetch_post_by_id(post_id):
        for post in blog_posts:
            if post['id'] == post_id:
                return post
        return None

    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('Author')
        post['title'] = request.form.get('Title')
        post['content'] = request.form.get('Content')

        with open('blog_posts.json', 'w', encoding='utf-8') as write_file:
            json.dump(blog_posts, write_file, indent=2)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
