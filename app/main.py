#!/usr/bin/python3
'''Starts a flask application for the app'''
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

api_url = 'https://geo.ipify.org/api/v2/country,city'
api_key = 'at_yIPGeKoiMSoTJaoxpCt1HKJK9X3Iw'


@app.route('/', strict_slashes=False)
def home():
    """Index page for application"""
    cache_id = str(uuid.uuid4())
    return render_template('index.html', cache_id=cache_id)


@app.route('/refresh')
def refresh():
    '''Redirects to the tracker page to return user information'''
    user_ip = session.get('extracted_user_ip')
    # Redirect to tracker with query parameter if user's IP is available
    if user_ip:
        print('refresh ip:', user_ip)
        return redirect(url_for('tracker', ip=user_ip))
    else:
        # Redirect without query parameter if user's IP is not available
        return redirect(url_for('tracker'))

@app.route('/tracker', strict_slashes=False, methods=['GET'])
def tracker():
    '''Tracker page for application'''
    cache_id = str(uuid.uuid4())
    ip_address = request.args.get('ip')
    domain_name = request.args.get('domain')
    user_ip = request.remote_addr
    print('Ip Address:', ip_address)
    print('Domain Name:', domain_name)
    print('user_ip:', user_ip)

    if not ip_address and not domain_name and not user_ip:
        return render_template('tracker.html', data=None, cache_id=cache_id)
    try:
        if ip_address:
            base_url = f'{api_url}?apiKey={api_key}&ipAddress={ip_address}'
        elif domain_name:
            base_url = f'{api_url}?apiKey={api_key}&domain={domain_name}'
        else:
            base_url = f'{api_url}?apiKey={api_key}&ipAddress={user_ip}'
        print(base_url)
        result = requests.get(base_url)
        data =  result.json()
        if 'code' in data:
            return render_template('tracker.html', error="Invalid IP address or domain name.", cache_id=cache_id)
        return render_template('tracker.html', data=data, request_method=request.method, cache_id=cache_id) 
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")


@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    if url:
        response = requests.get(url)
        return response.json()
    else:
        return jsonify({'error': 'URL parameter is missing'}), 400

@app.route('/extract_ip', methods=['POST'])
def extract_ip():
    ip_address = ''
    domain_name = ''

    if not request.is_json:
        # Handle form data
        form_input = request.form.get('ip_input')
        if form_input:
            ip_input = form_input
            if ip_input[0].isalpha():
                domain_name = ip_input
            else:
                ip_address = ip_input
        else:
            ip_address = None
            domain_name = None
    else:
        # Handle JSON request
        ip_input = request.json.get('ip_address')
        ip_address = ip_input
        session['extracted_user_ip'] = ip_address   
    
    session['extracted_ip'] = ip_address
    session['extracted_domain'] = domain_name
    

    # Log the received IP address
    print('Received IP address:', ip_address)
    print('Received Domain name:', domain_name)
    ext = session.get('extracted_user_ip')
    if ext:
        print('Received User Ip:', session['extracted_user_ip'])
    return redirect(url_for('tracker', ip=ip_address, domain=domain_name))

@app.route('/get_extracted_ip', methods=['GET'])
def get_extracted_ip():
    # Assuming extracted IP address is not in a session variable
    extracted_ip = session.get('extracted_ip')
    extracted_domain = session.get('extracted_domain')
    user_ip = session.get('extracted_user_ip')

    if extracted_ip:
        return jsonify({'ip_address': extracted_ip, 'domain_name': None, 'user_ip': user_ip})
    elif extracted_domain:
        return jsonify({'ip_address': None, 'domain_name': extracted_domain, 'user_ip': user_ip})
    else:
        return jsonify({'ip_address': None})
