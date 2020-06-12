from flask import Flask, render_template, request, url_for, redirect, flash
import json
import os.path as path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="awdjawd2r3r3d"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/short-url", methods=["GET", "POST"])
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
            return redirect(url_for('home'))
        if 'url' in request.form.keys():
            urls[short_url] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = short_url + secure_filename(f.filename)
            f.save('I:/Projects/url-shortener/' + full_name)
            urls[short_url] = {'file':full_name}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return render_template('short-url.html', code=short_url, serverurl='http://localhost:5000/')
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def short_path(code):
    urls = {}
    if path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(urls[code]['file'])
            else:
                flash('No such URL')
                return redirect(url_for('home'))
    else:
        flash('No data')
        return redirect(url_for('home'))