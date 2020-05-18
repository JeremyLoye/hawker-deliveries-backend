# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
import pymongo
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

@app.route('/listings/<date>', methods=["GET"])
def get_listing_by_date(date):
    return jsonify(fetch_listing(db, date))

@app.route('/listings/<date>/add', methods=["POST"])
def add_listing(date):
    if request.json:
        data = request.json
        try:
            inserted_id = insert_listing(db, date, data['code'], data['meal'])
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

@app.route('/listings/<date>/delete', methods=["POST"])
def remove_listing(date):
    try:
        return jsonify({
            "success": del_listing(db, date)
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
            modified = update_stall_availability(db, date, data['stallId'], data['available'])
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
            modified = update_food_quantity(db, date, data['stallId'], data['foodId'], data['quantity'])
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

@app.route('/listings/<date>/stall/<stallId>', methods=["GET"])
def get_stall_for_date(date, stallId):
    return jsonify(fetch_stall_for_date(db, stallId, date))

@app.route('/hawkercodes', methods=["GET"])
def get_hawker_codes():
    return jsonify([doc for doc in db.hawker.find({}, {"_id": 0, "name":1, "code": 1})])

@app.route('/stallcodes/<hawkercode>', methods=["GET"])
def get_stall_codes(hawkercode):
    return jsonify({
        "stalls": [doc for doc in db.stall.find({"location":hawkercode}, {"_id":0, "stallId":1, "name":1, "stallNo": 1})]
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
def check_payment_method():
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

@app.route('/main/<date>/product/<int:id>', methods=["GET", "POST"])
def test(date, id):
  storeList = [
  {
    'name': "Da Xi Hainanese Chicken Rice",
    'address': "21 Tanglin Road #01-58",
    'about': "Traditional chicken rice shop",
    'itemList': [
        {
            'id': "1",
            'name': "Roasted Chicken Rice",
            'image': "https://hawker-images.s3-ap-southeast-1.amazonaws.com/dummyimages/e5d685f5e24f9837e7dd22e2f8e1c617.jpg",
            'price': 3.50,
            'description': "Fragrant chicken rice with roasted chicken"
        },
        {
          'id': "2",
          'name': "Steamed Chicken Rice",
          'image': "https://hawker-images.s3-ap-southeast-1.amazonaws.com/dummyimages/chickenrice_566x424_fillbg_1b71b0de73.jpg",
          'price': 4.00,
          'description': "Fragrant chicken rice with roasted chicken"
      },
      {
        'id': "3",
        'name': "Thai Lemon Chicken Rice",
        'image': "https://hawker-images.s3-ap-southeast-1.amazonaws.com/dummyimages/2ebbb4a1a5e741b771f61620518_original_.jpg",
        'price': 4.50,
        'description': "Fragrant chicken rice with roasted chicken"
    }
    ]
  },
  {
    'name': "Ta Lu Prawn Noodles Stall",
    'address': "21 Tanglin Road #01-28",
    'about': "Specialty Prawn Noodles with a twist",
    'itemList': [
        {
            'id': "1",
            'name': "Prawn Noodles",
            'image': "https://cdn.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_450,h_300/https://danielfooddiary.com/wp-content/uploads/2019/05/prawnnoodles1.jpg",
            'price': 3.50,
            'description': "Fragrant chicken rice with roasted chicken"
        },
        {
          'id': "2",
          'name': "Short Rib Prawn Noodles",
          'image': "https://cdn.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_450,h_300/https://danielfooddiary.com/wp-content/uploads/2019/05/prawnnoodles1.jpg",
          'price': 4.00,
          'description': "Fragrant chicken rice with roasted chicken"
      }
    ]
  },
  {
    'name': "Wei Yi Laksa",
    'address': "21 Tanglin Road #01-89",
    'about': "Singapore's #1 Laksa",
    'itemList': [
        {
            'id': "1",
            'name': "Laksa (Small)",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'price': 3.00,
            'description': "Fragrant chicken rice with roasted chicken"
        },
        {
          'id': "2",
          'name': "Laksa (Medium)",
          'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
          'price': 3.50,
          'description': "Fragrant chicken rice with roasted chicken"
      },
      {
        'id': "3",
        'name': "Laksa (Large)",
        'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
        'price': 4.00,
        'description': "Fragrant chicken rice with roasted chicken"
    },
    {
          'id': "4",
          'name': "Specialty Laksa",
          'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
          'price': 4.50,
          'description': "Fragrant chicken rice with roasted chicken"
      },
      {
        'id': "5",
        'name': "Laksa Set with drink",
        'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
        'price': 5.00,
        'description': "Fragrant chicken rice with roasted chicken"
    }
    ]
  }]
  if id <= len(storeList):
      return storeList[id - 1]
  else:
      return {}

@app.route('/main/<date>', methods=["GET", "POST"])
def hawker_list(date):
    hawker_list =  {
        '14052020': [
            {
            'name': "Wei Yi Laksa",
            'id': "1",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'min_price': 4.50,
            'max_price': 6
            },
            {
            'name': "Da Xi Hainanese Chicken Rice",
            'id': "2",
            'image': "https://www.thespruceeats.com/thmb/vwIkJwmNwy55CJDYd11enCK5VB0=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/hainanese-chicken-rice-very-detailed-recipe-3030408-hero-0a742f08c72044e999202a44e30a1ea7.jpg",
            'min_price': 3.50,
            'max_price': 5.00
            },
            {
            'name': "Ta Lu Prawn Noodles Stall",
            'id': "3",
            'image': "https://cdn.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_450,h_300/https://danielfooddiary.com/wp-content/uploads/2019/05/prawnnoodles1.jpg",
            'min_price': 5,
            'max_price': 6
            }
        ],
        '15052020': [
            {
            'name': "Da Xi Hainanese Chicken Rice",
            'id': "1",
            'image': "https://www.thespruceeats.com/thmb/vwIkJwmNwy55CJDYd11enCK5VB0=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/hainanese-chicken-rice-very-detailed-recipe-3030408-hero-0a742f08c72044e999202a44e30a1ea7.jpg",
            'min_price': 3.50,
            'max_price': 5.00
            },
            {
            'name': "Ta Lu Prawn Noodles Stall",
            'id': "2",
            'image': "https://cdn.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_450,h_300/https://danielfooddiary.com/wp-content/uploads/2019/05/prawnnoodles1.jpg",
            'min_price': 5,
            'max_price': 6
            },
            {
            'name': "Wei Yi Laksa",
            'id': "3",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'min_price': 4.50,
            'max_price': 6
            }
        ],
        '16052020': [
            {
            'name': "Da Xi Hainanese Chicken Rice",
            'id': "1",
            'image': "https://www.thespruceeats.com/thmb/vwIkJwmNwy55CJDYd11enCK5VB0=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/hainanese-chicken-rice-very-detailed-recipe-3030408-hero-0a742f08c72044e999202a44e30a1ea7.jpg",
            'min_price': 3.50,
            'max_price': 5.00
            },
            {
            'name': "Wei Er Laksa",
            'id': "2",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'min_price': 5.50,
            'max_price': 7
            }
        ],
        '17052020': [
            {
            'name': "Da Xi Hainanese Chicken Rice",
            'id': "1",
            'image': "https://www.thespruceeats.com/thmb/vwIkJwmNwy55CJDYd11enCK5VB0=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/hainanese-chicken-rice-very-detailed-recipe-3030408-hero-0a742f08c72044e999202a44e30a1ea7.jpg",
            'min_price': 3.50,
            'max_price': 5.00
            },
            {
            'name': "Wei Er Laksa",
            'id': "2",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'min_price': 5.50,
            'max_price': 7
            },
            {
            'name': "Da Xi Hainanese Chicken Rice",
            'id': "3",
            'image': "https://www.thespruceeats.com/thmb/vwIkJwmNwy55CJDYd11enCK5VB0=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/hainanese-chicken-rice-very-detailed-recipe-3030408-hero-0a742f08c72044e999202a44e30a1ea7.jpg",
            'min_price': 3.50,
            'max_price': 5.00
            },
            {
            'name': "Singapore Famous Prawn Noodles Stall",
            'id': "4",
            'image': "https://cdn.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_450,h_300/https://danielfooddiary.com/wp-content/uploads/2019/05/prawnnoodles1.jpg",
            'min_price': 5,
            'max_price': 6
            },
            {
            'name': "Wei Yi Laksa",
            'id': "5",
            'image': "https://i2.wp.com/eatwhattonight.com/wp-content/uploads/2015/12/Laksa4.jpg?resize=1024%2C680&ssl=1",
            'min_price': 4.50,
            'max_price': 6
            }
        ]
    }
    if date in hawker_list:
        return jsonify({
            "products": hawker_list[date]
            })
    else:
        return jsonify({
            "products": []
        })
    

# We only need this for local development.
if __name__ == '__main__':
 app.run(debug=True)