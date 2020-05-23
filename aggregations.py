def aggregate_transaction_stall_price(db, date, meal, zone, stall_list):
    aggregation = db.transaction.aggregate([
        {
            "$match": {
                "$and": [
                    {"date": date},
                    {"meal": meal},
                    {"zone": zone},
                    {"cart.stallId": {
                        "$in": stall_list
                    }}
                ]
            }
        },
        {
            "$unwind": "$cart"
        },
        {
            "$match": {
                "cart.stallId": {
                    "$in": stall_list
                }
            }
        },
        {
            "$group": {
                "_id": "$cart.stallId",
                "total_price": {
                    "$sum": {
                        "$multiply": ["$cart.quantity", "$cart.price"]
                    }
                }
            }
        }
    ])
    return list(aggregation)

def aggregate_transaction_stall_qty(db, date, meal, zone, stall_list):
    aggregation = db.transaction.aggregate([
        {
            "$match": {
                "$and": [
                    {"date": date},
                    {"meal": meal},
                    {"zone": zone},
                    {"cart.stallId": {
                        "$in": stall_list
                    }}
                ]
            }
        },
        {
            "$unwind": "$cart"
        },
        {
            "$match": {
                "cart.stallId": {
                    "$in": stall_list
                }
            }
        },
        {
            "$group": {
                "_id": "$cart.stallId",
                "total_qty": {
                    "$sum": "$cart.quantity"
                }
            }
        }
    ])
    return list(aggregation)