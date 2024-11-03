receive_bp = Blueprint('receive', __name__)

@receive_bp.route('/receive_inventory', methods=['POST'])
def receive_inventory():
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    
    item = cluster.find_item(item_id)
    if item:
        cluster.update_quantity(item_id, quantity)
    else:
        cluster.insert_item({"item_id": item_id, "quantity": quantity, "status": "Available"})
    
    return jsonify({"message": "Inventory received"})

# picking.py
from flask import Blueprint, request, jsonify
import cluster

pick_bp = Blueprint('pick', __name__)

@pick_bp.route('/pick_inventory', methods=['POST'])
def pick_inventory():
    data = request.json
    order_id = data.get("order_id")
    items = data.get("items")
    
    for item in items:
        item_id = item["item_id"]
        quantity_needed = item["quantity"]
        
        inventory_item = cluster.find_item(item_id)
        if inventory_item and inventory_item["quantity"] >= quantity_needed:
            cluster.update_quantity(item_id, -quantity_needed)
        else:
            return jsonify({"error": f"Insufficient stock for item {item_id}"}), 400
    
    # Assuming an orders collection for updating order status
    db['orders'].update_one({"order_id": order_id}, {"$set": {"status": "Picked"}})
    return jsonify({"message": "Order picked successfully"})

# shipping.py
from flask import Blueprint, request, jsonify
import cluster

ship_bp = Blueprint('ship', __name__)

@ship_bp.route('/pack_inventory', methods=['POST'])
def pack_inventory():
    data = request.json
    order_id = data.get("order_id")
    carton_id = data.get("carton_id")
    
    # Mark the order as packed and associate it with a carton
    db['orders'].update_one({"order_id": order_id}, {"$set": {"status": "Packed", "carton_id": carton_id}})
    return jsonify({"message": "Order packed into carton"})

# app.py
from flask import Flask
from receiving import receive_bp
from picking import pick_bp
from shipping import ship_bp

app = Flask(__name__)
app.register_blueprint(receive_bp)
app.register_blueprint(pick_bp)
app.register_blueprint(ship_bp)

if __name__ == "__main__":
    app.run(debug=True)
