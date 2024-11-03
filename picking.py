from cluster import orders, act_inv

def pick_orders():
    # Find orders with status "Created" that are ready to be picked
    existing_orders = list(orders.find({"status": "Created"}))

    if not existing_orders:
        print("No orders available for picking.")
        return

    for order in existing_orders:
        print(f"\nProcessing Order ID: {order['order_id']}")

        for item in order["items"]:
            upc = item["upc"]
            quantity_needed = item["quantity"]

            # Check stock in active inventory
            inventory_item = act_inv.find_one({"upc": upc})

            # Prompt for location confirmation
            while True:
                location_input = input(f"Item UPC: {upc}, Quantity needed: {quantity_needed}. Please confirm the location: {inventory_item['location']} ")
                if location_input.strip() == inventory_item["location"]:
                    break
                else:
                    print(f"Location mismatch. Please try again.")

            # Prompt for UPC confirmation
            while True:
                upc_input = input("Please confirm the UPC you want to pick: ")
                if upc_input.strip() == upc:
                    break
                else:
                    print(f"UPC mismatch. Please try again.")

            # Prompt for quantity confirmation
            while True:
                quantity_input = input(f"Please confirm the quantity to pick (Needed: {quantity_needed}): ")
                if quantity_input.isdigit() and int(quantity_input) == quantity_needed:
                    break
                else:
                    print(f"Quantity mismatch. Expected: {quantity_needed}. Please try again.")

            # Deduct quantity from inventory
            act_inv.find_one_and_update(
                {"upc": upc},
                {"$inc": {"quantity": -quantity_needed}}
            )

        # Update order status to "Picked"
        orders.update_one({"order_id": order["order_id"]}, {"$set": {"status": "Picked"}})
        print(f"Order {order['order_id']} picking completed. Please stage for packing.")

def main():
    print("Warehouse Management System - Picking Process")
    user_input = input("Begin picking process? (yes/no): ").strip().lower()
    if user_input == "yes":
        pick_orders()
    else:
        print("Logging off.")

if __name__ == "__main__":
    main()
