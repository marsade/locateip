#!/usr/bin/python3
'''Starts a flask application for the app'''
from flask import Flask, render_template, request, session, redirect, url_for
import requests
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

api_url = 'https://geo.ipify.org/api/v2/country,city'
api_key = 'at_j8RdjZzkypr6I4XbJmSjafMq5pV4N'


@app.route('/', strict_slashes=False)
def home():
    """Index page for application"""
    return render_template('index.html')


@app.route('/refresh')
def refresh():
    '''Redirects to the tracker page to return user information'''
    url = f'{api_url}?apiKey={api_key}'
    return redirect(url_for('tracker'))


@app.route('/tracker', strict_slashes=False, methods=['GET', 'POST'])
def tracker():
    '''Tracker page for application'''
    
    if 'ip_address' in session:
        ip_address = session['ip_address']
    else:
        ip_address = None

    if 'domain_name' in session:
        domain_name = session['domain_name']
    else:
        domain_name = None

    if request.method == 'POST':
        ip_input = request.form.get('ip_input')
        if ip_input:
            if ip_input[0].isalpha():
                domain_name = ip_input
                session['domain_name'] = ip_input  # Store Domain name in session
            else:
                ip_address = ip_input
                session['ip_address'] = ip_input  # Store IP address in session
        else:
            # Clear IP address and Domain name if input is empty
            ip_address = None
            domain_name = None
            session.pop('ip_address', None)
            session.pop('domain_name', None)
    elif request.method == 'GET':
        ip_address = None
        domain_name = None

    try:
        if ip_address:
            base_url = f'{api_url}?apiKey={api_key}&ipAddress={ip_address}'
        elif domain_name:
            base_url = f'{api_url}?apiKey={api_key}&domain={domain_name}'
        else:
            base_url = f'{api_url}?apiKey={api_key}'
        result = requests.get(base_url)
        data =  result.json()
        return render_template('tracker.html', data=data, request_method=request.method)    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
