from pymongo import MongoClient
import key

cluster = f"mongodb+srv://jonfulk:{key.key}@cluster0.m6ewe.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(cluster)

#print(client.list_database_names())

db = client.test

act_inv = db['active_inventory']
inactive = db['inactive_inventory']
orders = db["orders"]

# add an item to inventory
def add_inventory_item(upc, quantity, location, reserved):
    
    item = {
        "upc": upc,
        "quantity": quantity,
        "location": location,
        "reserved": reserved
    }
    result = act_inv.insert_one(item)
    return result.inserted_id if result else None

def find_item(upc):
    return act_inv.find_one({"upc": upc})

def update_quantity(upc, quantity):
    return act_inv.update_one({"upc": upc}, {"$inc": {"quantity": quantity}})


def insert_item(item_data):
    return act_inv.insert_one(item_data)

# we use this to move item to inactive after shipping is complete
def move_to_inactive(upc, quantity):
    item = act_inv.find_one({"upc": upc})
    if item and item["quantity"] >= quantity:
        inactive.insert_one(item)
        return act_inv.delete_one({"upc": upc})
    return None

def generate_test_orders():
    # Retrieve some items from active_inventory
    items = list(act_inv.find().limit(3))
    
    if len(items) < 2:
        print("Not enough items in active inventory to generate test orders.")
        return

    # Order 1: Single item
    order_1 = {
        "order_id": "TEST_ORDER_1",
        "items": [
            {"upc": items[0]["upc"], "quantity": 2}
        ],
        "status": "Created",
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
            {"upc": items[1]["upc"], "quantity": 1}
        ],
        "status": "Created",
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

    # Insert orders into the orders collection
    orders.insert_many([order_1, order_2, order_3])

    print("Three test orders generated successfully.")