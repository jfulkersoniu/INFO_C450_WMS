import cluster
from cluster import db

def test_pack_inventory():
    order_id = input("Enter order ID to pack: ")
    carton_id = input("Enter carton ID: ")
    
    # Update order status to Packed
    db['orders'].update_one({"order_id": order_id}, {"$set": {"status": "Packed", "carton_id": carton_id}})
    print(f"Order {order_id} packed into carton {carton_id}")

if __name__ == "__main__":
    test_pack_inventory()
