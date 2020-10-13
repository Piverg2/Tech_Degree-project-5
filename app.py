from flask import (Flask, render_template, redirect, url_for, g, flash)

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


app = Flask(__name__)
app.secret_key = 'azwsxrdfctvghybujnikmol[rdfoijonhlkmwe;'
forms.csrf.init_app(app)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route("/")
def index():
    stream = models.Entry.select().limit(4)
    return render_template("index.html", stream=stream)


@app.route("/entries")
def entries():
    stream = models.Entry.select().limit(4)
    return render_template("index.html", stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
def create():
    """create new entry"""
    form = forms.JournalEntryForm()
    if form.validate_on_submit():
        models.Entry.create(title=form.title.data, date=form.date.data,
                            timespent=form.timespent.data,
                            post=form.content.data.strip(),
                            resources=form.resources.data.strip())
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    else:
        return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def details(id):
    """show the details of an entry"""
    post = models.Entry.get(models.Entry.entry_id == id)
    return render_template('detail.html', post=post)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    """Edit an entry"""
    form = forms.JournalEntryForm()
    post = models.Entry.get(models.Entry.entry_id == id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.date = form.date.data
        post.timespent = form.timespent.data
        post.content = form.content.data.strip()
        post.resources = form.resources.data.strip()
        post.save()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, post=post)


@app.route('/entries/<int:id>/delete')
def delete(id):
    """delete an entry"""
    entry = models.Entry.get(models.Entry.entry_id == id)
    entry.delete_instance()
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
