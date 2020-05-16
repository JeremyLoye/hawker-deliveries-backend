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


@app.route('/hawkers')
def get_all_hawkers():
    return jsonify({
        "hawkers": fetch_all_hawkers(db)
    })

@app.route('/hawkers/code/<code>')
def get_hawker_by_code(code):
    return jsonify(fetch_hawker_by_code(db, code))

@app.route('/stalls/stallId/<id>')
def get_stall_by_id(id):
    return jsonify(fetch_stall_by_id(db, id))

@app.route('/stalls/location/<location>')
def get_stalls_by_location(location):
    return jsonify({
        "stalls": fetch_stalls_by_location(db, location)
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