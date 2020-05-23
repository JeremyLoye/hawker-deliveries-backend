# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
from flask_pymongo import pymongo
from functions import *

config = configparser.ConfigParser()
config.read("credentials.ini")

client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0-fbceu.mongodb.net/test?retryWrites=true&w=majority".format(config['MONGO']['user'], config['MONGO']['password']))
db = client.hawkerv1

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET", "POST"])
def main_page():
    return '<h1>Hawker Deliveries</h1>'

@app.route('/listings', methods=["GET"])
def get_all_listings():
    return jsonify({
        "listings": fetch_all_listings(db)
    })

@app.route('/listings/get/<date>/<meal>/<zone>')
def get_listing_date_meal_zone(date, meal, zone):
    return jsonify(fetch_listing_date_meal_zone(db, date, meal, zone))

@app.route('/listings/<date>/<meal>', methods=["GET"])
def get_listing_by_date(date, meal):
    return jsonify(fetch_listing(db, date, meal))

@app.route('/listings/<date>/add', methods=["POST"])
def add_listing(date):
    if request.json:
        data = request.json
        try:
            # Remove later when handled
            if 'zone' not in data:
                zone = "Tembusu"
            else:
                zone = data['zone']
            inserted_id = insert_listing(db, date, data['code'], data['meal'], zone)
            return jsonify({
                "success": str(inserted_id)
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/listings/<date>/<meal>/<zone>/delete', methods=["POST"])
def remove_listing(date, meal, zone):
    try:
        return jsonify({
            "success": del_listing(db, date, meal, zone)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/listings/<date>/availability', methods=["POST"])
def update_availability(date):
    if request.json:
        data = request.json
        try:
            modified = update_stall_availability(db, date, data['stallId'], data['meal'], data['zone'], data['available'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/listings/<date>/quantity', methods=["POST"])
def update_quantity(date):
    if request.json:
        data = request.json
        try:
            modified = update_food_quantity(db, date, data['stallId'], data['foodId'], data['meal'], data['zone'], data['quantity'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/listings/<date>/<meal>/<zone>/stall/<stallId>', methods=["GET"])
def get_stall_for_date_meal_zone(date, meal, zone, stallId):
    try:
        return jsonify(fetch_stall_for_date_meal_zone(db, date, meal, zone, stallId))
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/hawkercodes', methods=["GET"])
def get_hawker_codes():
    return jsonify([doc for doc in db.hawker.find({}, {"_id": 0, "name":1, "code": 1})])

@app.route('/stallcodes/<hawkercode>', methods=["GET"])
def get_stall_codes(hawkercode):
    return jsonify({
        "stalls": [doc for doc in db.stall.find({"location":hawkercode}, {"_id":0, "stallId":1, "name":1, "stallNo": 1}, sort=[("stallId",1)])]
    })

@app.route('/hawkers')
def get_all_hawkers():
    return jsonify({
        "hawkers": fetch_all_hawkers(db)
    })

@app.route('/hawkers/<code>')
def get_hawker_by_code(code):
    return jsonify(fetch_hawker_by_code(db, code))

@app.route('/hawkers/<code>/add', methods=["POST"])
def add_hawker(code):
    if request.json:
        data = request.json
        try:
            inserted_id = insert_hawker(db, data['name'], code, data['address'], data['image'])
            return jsonify({
                "success": str(inserted_id)
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else: 
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/hawkers/<code>/delete', methods=["POST"])
def remove_hawker(code):
    try:
        return jsonify({
            "success": del_hawker(db, code)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/hawkers/<code>/update', methods=["POST"])
def update_hawker_info(code):
    if request.json:
        data = request.json
        try:
            updated_obj = update_hawker(db, code, data)
            updated_obj.pop("_id", None)
            return jsonify({
                "success": updated_obj
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/hawkers/<code>/stalls', methods=["GET"])
def get_stalls_by_hawker(code):
    return jsonify({
        "stalls": fetch_stalls_by_location(db, code)
    })

@app.route('/stalls/<id>')
def get_stall_by_id(id):
    return jsonify(fetch_stall_by_id(db, id))

@app.route('/stalls/insert', methods=["POST"])
def add_stall():
    if request.json:
        data = request.json
        try:
            inserted_id = insert_stall(db, data['name'], data['type'], data['location'], data['image'], data['stallNo'], data['food'], data['about'], data['contact'])
            return jsonify({
                "success": str(inserted_id)
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })    

@app.route('/stalls/<stallId>/delete', methods=["POST"])
def remove_stall(stallId):
    try:
        return jsonify({
            "success": del_stall(db, stallId)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/stalls/<stallId>/update', methods=["POST"])
def update_stall_info(stallId):
    if request.json:
        data = request.json
        try:
            updated_obj = update_stall(db, stallId, data)
            updated_obj.pop("_id", None)
            return jsonify({
                "success": updated_obj
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/users/<userId>', methods=["POST"])
def get_user(userId):
    return jsonify(fetch_user(db, userId))

@app.route('/users/add', methods=["POST"])
def add_user():
    if request.json:
        data = request.json
        try:
            inserted_id = insert_user(db, data['awsId'], data['name'], data['phone'], data['email'], data['payment'])
            return jsonify({
                "success": str(inserted_id)
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/users/payment/check', methods=["POST"])
def verify_payment_method():
    if request.json:
        data = request.json
        try:
            return jsonify({
                "available": check_payment_method(db, data['method'], data['username'])
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/users/payment/add', methods=["POST"])
def add_user_payment():
    if request.json:
        data = request.json
        try:
            modified = insert_user_payment(db, data['awsId'], data['method'], data['username'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/users/payment/delete', methods=["POST"])
def remove_user_payment():
    if request.json:
        data = request.json
        try:
            modified = delete_user_payment(db, data['awsId'], data['method'], data['username'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/users/payment/update', methods=["POST"])
def update_payment():
    if request.json:
        data = request.json
        try:
            modified = update_user_payment(db, data['awsId'], data['method'], data['username'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

"""
TRANSACTIONS
"""
@app.route('/transactions/get/<date>/<meal>/<zone>', methods=["POST"])
def get_transactions_date_meal_zone(date, meal, zone):
    try:
        return jsonify({
            "transactions": fetch_transactions_date_meal_zone(db, date, meal, zone)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/transactions/datemeal/<date>/<meal>', methods=["POST"])
def get_transaction_by_date_meal(date, meal):
    try:
        return jsonify({
            "transactions": fetch_transactions_by_date_meal(db, date, meal)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/transactions/user', methods=["POST"])
def get_transactions_by_user():
    if request.json:
        data = request.json
        try:
            return jsonify({
                "transactions": fetch_transactions_for_user(db, data['awsId'])
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/transactions/add', methods=["POST"])
def add_transaction():
    if request.json:
        data = request.json
        try:
            # Removed when handled
            if 'zone' in data:
                zone = data['zone']
            else:
                zone = "Tembusu"
            inserted_id = insert_transaction(db, data['awsId'], data['date'], data['cart'], data['paymentMethod'], data['paymentUsername'], data['meal'], zone)
            return jsonify({
                "success": str(inserted_id)
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

@app.route('/transactions/update', methods=["POST"])
def update_transaction_paid():
    if request.json:
        data = request.json
        try:
            modified = update_transaction(db, data['_id'], data['paid'])
            return jsonify({
                "success": modified
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            })
    else:
        return jsonify({
            "error": "No request body provided"
        })

# We only need this for local development.
if __name__ == '__main__':
 app.run(debug=True)