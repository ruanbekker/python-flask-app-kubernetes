from flask import Flask
from socket import gethostname
import logging
import pytest

app = Flask(__name__)
app.config['DEBUG'] = False

def generate_hello_message():
    hostname = gethostname()
    message = f"hello from {hostname}"
    return message

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    
@app.route('/')
def home():
    message = generate_hello_message()
    return message

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
