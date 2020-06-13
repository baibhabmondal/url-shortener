from flask import render_template, request, url_for, redirect, flash, abort, session, jsonify, Blueprint
import json
import os.path as path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@bp.route("/short-url", methods=["GET", "POST"])
def user():
    short_url = request.form['code']
    if request.method == 'POST':
        urls = {}
        if path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if short_url in urls.keys():
            # print('same')
            flash("The short name already exists. Pick something else.")
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[short_url] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = short_url + secure_filename(f.filename)
            f.save('I:/Projects/url-shortener/urlshort/static/user_files/' + full_name)
            urls[short_url] = {'file':full_name}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[short_url] = True
        return render_template('short-url.html', code=short_url, serverurl='http://localhost:5000/')
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/api/session')
def session_keys():
    return jsonify(list(session.keys()))

@bp.route('/<string:code>')
def short_path(code):
    urls = {}
    if path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('notfound.html', serverurl="http://localhost:5000"), 404

