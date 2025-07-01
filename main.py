from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, flash
from post import create_post, get_all_posts, get_post_by_id, update_post, delete_post

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    titulo = "Este es el html home como variable"
    return render_template('home.html', titulo=titulo)

@app.route('/posts')
def show_all_posts():
    posts = get_all_posts()
    return render_template('post/post_list.html', posts=posts)

@app.route('/posts/<int:post_id>')
def get_one_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        abort(404)
    return render_template('post/post.html', post=post)

@app.route('/posts/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('post/create.html')
    
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Título y contenido no pueden estar vacíos.", "error")
        return render_template("post/create.html", title=title, content=content)

    create_post(title, content)
    flash("Post creado correctamente.", "success")
    return redirect(url_for("show_all_posts"))

@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_one_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        abort(404)

    if request.method == 'GET':
        return render_template('post/edit.html', post=post)
    
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Título y contenido no pueden estar vacíos.", "error")
        return render_template("post/edit.html", post=post)

    update_post(post_id, title, content)
    flash("Post actualizado correctamente.", "success")
    return redirect(url_for("show_all_posts"))

@app.route('/posts/delete/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    delete_post(post_id)
    flash("Post eliminado correctamente.", "success")
    return "", 200

@app.route('/api/new')
def api():
    datos = [
        {"nombre": "Jorge", "edad": 35, "trabaja": True},
        {"nombre": "Jaime", "edad": 34, "trabaja": False},
    ]
    return jsonify(datos), 200

if __name__ == '__main__':
    app.run(debug=True)
