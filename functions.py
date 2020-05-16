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
    return inserted_stall

def del_stall(db, stallId):
    return db.stall.delete_one({"stallId": stallId}).deleted_count

def update_stall(db, stallId, stall):
    return db.stall.find_one_and_update({"stallId": stallId}, {"$set": stall})