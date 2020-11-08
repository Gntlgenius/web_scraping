from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    resp = requests.get(
        url = 'http://127.0.0.1:9080/crawl.json?start_requests=true&spider_name=reviews_L'
    ).json()

    items = resp.get('items')

    return render_template('index.html', reviews = items)
    
@app.route('/show')
def show_page():
    features = ['REVIEWS','SUMMARY CAPTION','RATINGS']
    return render_template('index.html', site_features = features)






if __name__ == '__main__':
    app.run(debug=True)