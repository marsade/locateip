#!/usr/bin/python3
'''Starts a flask application for the app'''
from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Index page for application"""
    return render_template('index.html')

@app.route('/tracker', strict_slashes=False, methods=['GET', 'POST'])
def tracker():
    '''Tracker page for application'''
    api_url = 'https://geo.ipify.org/api/v2/country,city'
    api_key = 'at_j8RdjZzkypr6I4XbJmSjafMq5pV4N'
    try:
        if request.method == 'GET':
            base_url = f'{api_url}?apiKey={api_key}'
            result = requests.get(base_url)
            data =  result.json()
            return render_template('tracker.html', data=data)

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
