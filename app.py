# app.py

from flask import Flask
from flask_cors import CORS
import configparser
import pymongo

config = configparser.ConfigParser()
config.read("credentials.ini")

client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0-fbceu.mongodb.net/test?retryWrites=true&w=majority".format(config['MONGO']['user'], config['MONGO']['password']))
db = client.hawkerv1

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET", "POST"])
def main_page():
 return '<h1>Hawker Delivery API</h1>'

# We only need this for local development.
if __name__ == '__main__':
 app.run()