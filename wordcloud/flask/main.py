from flask import Flask, render_template, request
from word import create_cloud

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result/', methods=['GET', 'POST'])
def get_result():
    texts = str(request.form['texts'])
    language = str(request.form['language'])
    create_cloud(texts, language)
    return render_template('result.html')


if __name__ == '__main__':
    app.run()
