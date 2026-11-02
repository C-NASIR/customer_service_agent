ORDERS = {
    "123": {
        "status": "shipped", 
        "arrival": "friday"
    },
    "456": {
        "status": "processing", 
        "arrival": None
    }
}

def get_order(order_id):
    return ORDERS.get(order_id, {"error": "no order found"})
