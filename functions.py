import datetime

"""
dailyListing functions
"""
def fetch_all_listings(db, _id=0):
    today = datetime.datetime.now().strftime("%d%m%Y")
    return [doc for doc in db.dailyListing.find({"date": {"$gte": today}}, {"_id": _id})]

def fetch_listing(db, date, _id=0):
    return db.dailyListing.find_one({"date": date}, {"_id": _id})

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
            "available": True,
            "food": [{**food, 'quantity': -1} for food in stall['food'] if food['available']]
        })
    listing['orderAvailable'] = orderAvailable
    listing['meal'] = meal
    return db.dailyListing.insert_one(listing).inserted_id

def del_listing(db, date):
    return db.dailyListing.delete_one({"date": date}).deleted_count

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
    return db['hawker'].insert_one({
        "name": name,
        "code": code,
        "address": address,
        "image": image
    })

def update_hawker(db, code, mapping):
    return db.hawker.update_one({"code": "THM"}, {"$set": mapping}).modified_count

"""
stall functions
"""
def fetch_stall_by_id(db, stallId, _id=0):
    return db.stall.find_one({"stallId": stallId}, {"_id": _id})

def fetch_stalls_by_location(db, location, _id=0):
    return [doc for doc in db.stall.find({"location": location}, {"_id": _id})]

def insert_stall(db, name, stall_type, location, stallNo, food, about, contact):
    stallId = "{}_{}".format(location, stallNo)
    if fetch_stall_by_id(db, stallId):
        raise Exception("Store already exists!")
    stall = {
        "name": name,
        "type": stall_type,
        "location": location,
        "stallNo": stallNo,
        "stallId": stallId,
        "food": food,
        "about": about,
        "contact": contact
    }
    inserted_stall = db['stall'].insert_one(stall).inserted_id
    return inserted_stall, modified_hawker