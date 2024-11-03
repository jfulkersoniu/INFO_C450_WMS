from cluster import generate_test_orders

def main():
    print("Warehouse Management System - Daily Order Waving")
    print("------------------------------------------------")
    
    # Simulate waving orders each day by generating test orders
    user_input = input("Would you like to generate orders for the day? (yes/no): ").strip().lower()
    if user_input == "yes":
        generate_test_orders()
        print("Test orders have been successfully generated and are ready for picking.")
    else:
        print("No orders were generated today.")

if __name__ == "__main__":
    main()