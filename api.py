# flaskapi.py
from datetime import datetime

from flask import Flask, jsonify, request
from scraper import scrape_with_date  # Import the scraping function

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    date = request.args.get('date', default=datetime.today().strftime('%Y-%m-%d'), type=str)
    data = scrape_with_date(date)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
