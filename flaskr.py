from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from database import db_session
from models import Entry
# from werkzeug import url_decode


# class MethodRewriteMiddleware(object):

#     def __init__(self, app):
#         self.app = app

#     def __call__(self, environ, start_response):
#         if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
#             args = url_decode(environ['QUERY_STRING'])
#             method = args.get('__METHOD_OVERRIDE__')
#             if method:
#                 method = method.encode('ascii', 'replace')
#                 environ['REQUEST_METHOD'] = method
#         return self.app(environ, start_response)


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'PUT'])
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(request.form['title'], request.form['text'])
    db_session.add(entry)
    db_session.commit()
    flash(u'New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/delete/<int:entry_id>', methods=['POST', 'DELETE'])
def delete_entry(entry_id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.query.filter(Entry.id == entry_id).first()
    db_session.delete(entry)
    db_session.commit()
    flash(u'The entry was successfully deleted')
    return redirect(url_for('show_entries'))


@app.route('/edit/<int:entry_id>')
def edit_entry(entry_id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.query.filter(Entry.id == entry_id).first()
    return render_template('show_entry.html', entry=entry)


@app.route('/edit/<int:entry_id>', methods=['POST', 'PUT'])
def update_entray(entry_id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.query.filter(Entry.id == entry_id).first()
    entry.title, entry.text = request.form['title'], request.form['text']
    db_session.commit()
    flash(u'The entry was successfully updated')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
