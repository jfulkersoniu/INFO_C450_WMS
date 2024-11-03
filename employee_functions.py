'''
Warehouse Management System
Written by Jonathan Fulkerson
'''

# Import statements
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask (__name__)
inventory = db['inventory']

# Functions
# Receive Inventory
@app.route('/receive_inventory', methods=['POST'])
def receive_inventory():
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    
    item = inventory.find_one({"item_id": item_id})
    if item:
        # Update quantity if item exists
        inventory.update_one(
            {"item_id": item_id},
            {"$inc": {"quantity": quantity}}
        )
    else:
        # Insert new item
        inventory.insert_one({
            "item_id": item_id,
            "quantity": quantity,
            "status": "Available"
        })
    
    return jsonify({"message": "Inventory received"})

# Perform Picking
@app.route('/pick_inventory', methods=['POST'])
def pick_inventory():
    data = request.json
    order_id = data.get("order_id")
    items = data.get("items")
    
    # Check stock and update inventory
    for item in items:
        item_id = item["item_id"]
        quantity_needed = item["quantity"]
        
        inventory_item = inventory.find_one({"item_id": item_id})
        if inventory_item and inventory_item["quantity"] >= quantity_needed:
            # Deduct quantity from inventory
            inventory.update_one(
                {"item_id": item_id},
                {"$inc": {"quantity": -quantity_needed}}
            )
        else:
            return jsonify({"error": f"Insufficient stock for item {item_id}"}), 400
    
    # Mark order as picked
    orders.update_one({"order_id": order_id}, {"$set": {"status": "Picked"}})
    return jsonify({"message": "Order picked successfully"})


# Perform Packing
@app.route('/pack_inventory', methods=['POST'])
def pack_inventory():
    data = request.json
    order_id = data.get("order_id")
    carton_id = data.get("carton_id")
    
    # Associate carton with order items
    orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": "Packed", "carton_id": carton_id}}
    )
    
    return jsonify({"message": "Order packed into carton"})

def generate_test_orders():
    # Retrieve some items from active_inventory
    items = list(active_inventory.find().limit(3))
    
    if len(items) < 2:
        print("Not enough items in active inventory to generate test orders.")
        return

    # Order 1: Single item
    order_1 = {
        "order_id": "TEST_ORDER_1",
        "items": [
            {"item_id": items[0]["item_id"], "quantity": 2}
        ],
        "status": "Created",
        "created_at": datetime.now(),
        "packed_at": None,
        "shipped_at": None,
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 1",
            "address": "123 Test St, Test City, Country",
            "contact": "555-0001"
        }
    }

    # Order 2: Another single item
    order_2 = {
        "order_id": "TEST_ORDER_2",
        "items": [
            {"item_id": items[1]["item_id"], "quantity": 1}
        ],
        "status": "Created",
        "created_at": datetime.now(),
        "packed_at": None,
        "shipped_at": None,
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 2",
            "address": "456 Sample Ave, Sample City, Country",
            "contact": "555-0002"
        }
    }

    # Order 3: Two different items
    order_3 = {
        "order_id": "TEST_ORDER_3",
        "items": [
            {"item_id": items[0]["item_id"], "quantity": 1},
            {"item_id": items[1]["item_id"], "quantity": 3}
        ],
        "status": "Created",
        "created_at": datetime.now(),
        "packed_at": None,
        "shipped_at": None,
        "carton_id": None,
        "customer_details": {
            "name": "Test Customer 3",
            "address": "789 Example Rd, Example City, Country",
            "contact": "555-0003"
        }
    }

    # Insert orders into the orders collection
    orders.insert_many([order_1, order_2, order_3])

    print("Three test orders generated successfully.")

# Run function to generate test orders
generate_test_orders()