#!/usr/bin/python3
from app import main

if __name__ == '__main__':
    main.app.run(host='0.0.0.0', port=5000, debug=True)