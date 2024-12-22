from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
import key

cluster = f"mongodb+srv://jonfulk:{key.key}@cluster0.m6ewe.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(cluster)

db = client.test

act_inv = db['active_inventory']
inactive = db['inactive_inventory']
orders = db["orders"]
users = db["users"]

def add_inventory_item(upc, quantity, location, reserved):
    item = {
        "upc": upc,
        "quantity": quantity,
        "location": location,
        "reserved": reserved
    }
    result = act_inv.insert_one(item)
    return result.inserted_id if result else None

def authenticate_user(username, password):
    user = db['users'].find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return user
    return None

def confirm_pick(order_id, confirmations):
    for confirmation in confirmations:
        upc = confirmation["upc"]
        confirmed_quantity = confirmation["quantity_confirmed"]

        act_inv.find_one_and_update(
            {"upc": upc},
            {"$inc": {"quantity": -confirmed_quantity}}
        )

    orders.update_one({"order_id": order_id}, {"$set": {"status": "Picked"}})

    return {"success": True, "message": f"Order {order_id} successfully picked."}

def create_user(username, department, password):
    hashed_password = generate_password_hash(password)
    user_data = {
        'username': username,
        'department': department,
        'password': hashed_password
    }
    result = db['users'].insert_one(user_data)
    if result.inserted_id:
        return {'status': 'success', 'message': f'User {username} created successfully.'}
    return {'status': 'error', 'message': 'Failed to create user.'}

def find_item(upc):
    return act_inv.find_one({"upc": upc})

def find_picked_order():
    order = orders.find_one({"status": "Picked"}, sort=[("order_id", 1)])
    if not order:
        return {"error": "No orders available for packing."}

    order_details = {
        "order_id": order["order_id"],
        "items": order.get("items", []),
        "status": order["status"],
        "customer_details": order.get("customer_details", {})
    }

    print("Retrieved picked order:", order)
    return order_details

def pick_order():
    order = orders.find_one({"status": "Created"}, sort=[("order_id", 1)])
    if not order:
        return {"error": "No orders available for picking."}

    order_items = []
    for item in order.get("items", []):
        quantity = item.get("quantity")
        if isinstance(quantity, dict) and "$numberInt" in quantity:
            quantity = int(quantity["$numberInt"])

        inventory_item = act_inv.find_one({"upc": item["upc"]})
        location = inventory_item["location"] if inventory_item else "Unknown"
        
        order_items.append({"upc": item["upc"], "quantity": quantity, "location": location})

    order_details = {
        "order_id": order["order_id"],
        "order_items": order_items,
        "status": order["status"],
        "customer_details": order.get("customer_details", {})
    }

    print("Retrieved order:", order)
    return order_details

def pack_order(order_id, carton_id):
    order = orders.find_one({"order_id": order_id})
    if order is None:
        return {"error": f"Order with ID {order_id} does not exist."}

    if order['status'] != 'Picked':
        return {"error": f"Order {order_id} is not in 'Picked' status. Please pick the order first."}

    orders.update_one({"order_id": order_id}, {"$set": {"status": "Packed", "carton_id": carton_id}})
    print(f"Order {order_id} packed into carton {carton_id}")
    return {"success": True, "message": f"Order {order_id} successfully packed."}

def update_quantity(upc, quantity):
    return act_inv.update_one({"upc": upc}, {"$inc": {"quantity": quantity}})

def insert_item(item_data):
    return act_inv.insert_one(item_data)

def move_to_inactive(upc, quantity):
    item = act_inv.find_one({"upc": upc})
    if item and item["quantity"] >= quantity:
        inactive.insert_one(item)
        return act_inv.delete_one({"upc": upc})
    return None

def generate_test_orders():
    items = list(act_inv.find().limit(3))
    
    if len(items) < 2:
        print("Not enough items in active inventory to generate test orders.")
        return

    highest_order = orders.find_one(sort=[("order_id", -1)])
    last_order_id = int(highest_order["order_id"]) if highest_order else 0

    new_order_id_1 = f"{last_order_id + 1:08d}"
    new_order_id_2 = f"{last_order_id + 2:08d}"
    new_order_id_3 = f"{last_order_id + 3:08d}"

    order_1 = {
        "order_id": new_order_id_1,
        "items": [{"upc": items[0]["upc"], "quantity": 2}],
        "status": "Created",
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 1",
            "address": "123 Test St, Test City, Country",
            "contact": "555-0001"
        }
    }

    order_2 = {
        "order_id": new_order_id_2,
        "items": [{"upc": items[1]["upc"], "quantity": 1}],
        "status": "Created",
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 2",
            "address": "456 Sample Ave, Sample City, Country",
            "contact": "555-0002"
        }
    }

    order_3 = {
        "order_id": new_order_id_3,
        "items": [
            {"upc": items[0]["upc"], "quantity": 1},
            {"upc": items[1]["upc"], "quantity": 3}
        ],
        "status": "Created",
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 3",
            "address": "789 Example Rd, Example City, Country",
            "contact": "555-0003"
        }
    }

    print(f"Generated Order 1: {order_1}")
    print(f"Generated Order 2: {order_2}")
    print(f"Generated Order 3: {order_3}")

    orders.insert_many([order_1, order_2, order_3])
    print(f"Generated orders with IDs: {new_order_id_1}, {new_order_id_2}, {new_order_id_3}")
