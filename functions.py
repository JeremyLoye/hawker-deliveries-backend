import datetime
from bson.objectid import ObjectId

"""
dailyListing functions
"""
def fetch_all_listings(db, _id=0):
    today = datetime.datetime.now().strftime("%d%m%Y")
    return [doc for doc in db.dailyListing.find({"date": {"$gte": today}}, {"_id": _id})]

def fetch_listing(db, date, _id=0):
    listing = db.dailyListing.find_one({"date": date}, {"_id": _id})
    listing['stalls'].sort(key=lambda x: x['stallId'])
    listing['stalls'].sort(key=lambda x: x['available'], reverse=True)
    return listing

def insert_listing(db, date, code, meal, orderAvailable=True):
    if fetch_listing(db, date):
        raise Exception("Listing for this date already exists, use update instead!")
    listing = fetch_hawker_by_code(db, code)
    listing['date'] = date
    listing['stalls'] = []
    for stall in fetch_stalls_by_location(db, code):
        listing['stalls'].append({
            "stallId": stall['stallId'],
            "name": stall['name'],
            "type": stall['type'],
            "image": stall['image'],
            "available": True,
            "food": [{**food, 'quantity': -1} for food in stall['food'] if food['available']]
        })
    listing['orderAvailable'] = orderAvailable
    listing['meal'] = meal
    return db.dailyListing.insert_one(listing).inserted_id

def del_listing(db, date):
    return db.dailyListing.delete_one({"date": date}).deleted_count

def update_stall_availability(db, date, stallId, availability):
    listing = fetch_listing(db, date)
    if not listing:
        raise Exception("Listing unavailable for this date")
    if type(availability) != bool:
        raise Exception("Availability provided is not a boolean")
    stalls = listing['stalls']
    for stall in stalls:
        if stall['stallId'] == stallId:
            stall['available'] = availability
            updated = db.dailyListing.update_one({"date": date}, {"$set": {"stalls": stalls}}).modified_count
            return updated
    raise Exception("No such stall in this listing")

def update_food_quantity(db, date, stallId, foodId, quantity):
    listing = fetch_listing(db, date)
    if not listing:
        raise Exception("Listing unavailable for this date")
    stalls = listing['stalls']
    for stall in stalls:
        if stall['stallId'] == stallId:
            for food in stall['food']:
                if food['id'] == foodId:
                    food['quantity'] = int(quantity)
                    updated = db.dailyListing.update_one({"date": date}, {"$set": {"stalls": stalls}}).modified_count
                    return updated
    raise Exception("No such stall or food in this listing")

def fetch_stall_for_date(db, stallId, date, _id=0):
    stall = db.dailyListing.find_one({"date": date}, {"stalls": {"$elemMatch": {"stallId": stallId}}, "_id": _id})['stalls'][0]
    new_info = fetch_stall_by_id(db, stall['stallId'])
    stall['about'] = new_info['about']
    stall['contact'] = new_info['contact']
    stall['stallNo'] = new_info['stallNo']
    return stall

"""
hawker functions
"""
def fetch_all_hawkers(db, _id=0):
    hawkers = []
    for doc in db.hawker.find({}, {"_id": _id}):
        hawkers.append(doc)
    return hawkers

def fetch_hawker_by_code(db, code, _id=0):
    return db.hawker.find_one({"code": code}, {"_id": _id})

def insert_hawker(db, name, code, address, image):
    if fetch_hawker_by_code(db, code):
        raise Exception("Hawker with code {} already exists!".format(code))
    return db['hawker'].insert_one({
        "name": name,
        "code": code,
        "address": address,
        "image": image
    }).inserted_id

def del_hawker(db, code):
    return db.hawker.delete_one({"code": code}).deleted_count

def update_hawker(db, code, hawker):
    return db.hawker.find_one_and_update({"code": code}, {"$set": hawker})

"""
stall functions
"""
def fetch_stall_by_id(db, stallId, _id=0):
    return db.stall.find_one({"stallId": stallId}, {"_id": _id})

def fetch_stalls_by_location(db, location, _id=0):
    return [doc for doc in db.stall.find({"location": location}, {"_id": _id}, sort=[("stallId", 1)])]

def insert_stall(db, name, stall_type, location, image, stallNo, food, about, contact):
    stallId = "{}_{}".format(location, stallNo)
    if fetch_stall_by_id(db, stallId):
        raise Exception("Store already exists!")
    stall = {
        "name": name,
        "type": stall_type,
        "location": location,
        "image": image,
        "stallNo": stallNo,
        "stallId": stallId,
        "food": food,
        "about": about,
        "contact": contact
    }
    inserted_stall = db['stall'].insert_one(stall).inserted_id
    return inserted_stall

def del_stall(db, stallId):
    return db.stall.delete_one({"stallId": stallId}).deleted_count

def update_stall(db, stallId, stall):
    return db.stall.find_one_and_update({"stallId": stallId}, {"$set": stall})

"""
user functions
"""
import datetime

def insert_user(db, aws_id, name, phone, email, payment_accounts=[]):
    if fetch_user(db, aws_id):
        raise Exception("User with this ID already exists!")
    user = {
        "awsId": aws_id,
        "name": name,
        "phone": phone,
        "email": email,
        "payment": payment_accounts,
        "dateJoined": datetime.datetime.now()
    }
    inserted_user = db.user.insert_one(user).inserted_id
    return inserted_user
    
def fetch_user(db, aws_id, _id=0):
    return db.user.find_one({"awsId": aws_id}, {"_id": _id})

def check_payment_method(db, method, username):
    return len([x for x in db.user.find({"payment.method": method, "payment.username": username}, {"_id":1}).limit(1)])==0

def insert_user_payment(db, aws_id, method, username):
    if len([x for x in db.user.find({"awsId": aws_id, "payment.method": method}, {"_id": 1}).limit(1)]) > 0:
        raise Exception("Payment method {} already exists for user".format(method))
    return db.user.update_one({"awsId": aws_id}, {"$push": {"payment": {
        "method": method,
        "username": username
    }}}).modified_count

def delete_user_payment(db, aws_id, method, username):
    if len([x for x in db.user.find({"awsId": aws_id, "payment.method": method, "payment.username": username}, {"_id": 1}).limit(1)])==0:
        raise Exception("Payment method {} with this username does not exist for user".format(method))
    return db.user.update_one({"awsId": aws_id}, {"$pull": {"payment": {"method": method, "username": username}}}).modified_count

def update_user_payment(db, aws_id, method, username):
    if len([x for x in db.user.find({"awsId": aws_id, "payment.method": method}, {"_id": 1}).limit(1)])==0:
        raise Exception("Payment method {} does not exist for user".format(method))
    return db.user.update_one({"awsId": aws_id, "payment.method": method}, {"$set": {"payment.$.username": username}}).modified_count

"""
transaction functions
"""

def fetch_transactions_by_date_meal(db, date, meal):
    transactions = []
    for doc in db.transaction.find({"date": date, "meal": meal}):
        doc['_id'] = str(doc['_id'])
        transactions.append(doc)
    return transactions

def insert_transaction(db, awsId, date, cart, paymentMethod, paymentUsername, meal, paid=False):
    if not fetch_user(db, aws_id):
        raise Exception("User with this ID already exists!")
    transaction = {
        "dateTime": datetime.datetime.now(),
        "date": date,
        "awsId": awsId,
        "cart": cart,
        "paid": paid,
        "paymentMethod": paymentMethod,
        "paymentUsername": paymentUsername,
        "totalPrice": sum([food['price'] for food in cart]),
        "meal": meal
    }
    inserted_id = db.transaction.insert_one(transaction).inserted_id
    return inserted_id

def update_transaction(db, _id, paid):
    return db.transaction.update_one({"_id": ObjectId(_id)}, {"$set": {"paid": paid}}).modified_count

def fetch_transactions_for_user(db, awsId):
    transactions = []
    for doc in db.transaction.find({"awsId": awsId}, sort=[("dateTime", -1)]):
        doc['_id'] = str(doc['_id'])
        transactions.append(doc)
    return transactions