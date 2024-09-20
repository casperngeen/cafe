from flask import Flask, jsonify
from config import DbConfig

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)