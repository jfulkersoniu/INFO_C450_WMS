import cluster

def test_receive_inventory():
    while True:
        upc = input("Enter item ID to receive: ")
        quantity = int(input("Enter quantity to receive: "))
        location = input("Enter the location this item was put away to: ")
        
        # Insert the item into the inventory
        cluster.insert_item({"upc": upc, "quantity": quantity, "location": location, "reserved": False})
        print(f"{quantity} of item {upc} put away in location {location}")

        # Prompt the user to continue or exit
        continue_prompt = input("Would you like to receive another item? (yes/no): ").strip().lower()
        if continue_prompt != 'yes':
            print("Exiting the receive inventory process.")
            break

if __name__ == "__main__":
    test_receive_inventory()