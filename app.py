from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run( port=50010, host='0.0.0.0')