import pymongo
import requests

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://your_username:your_password@cluster0.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
collection = db['data_collection']

def fetch_external_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {api_url}")
        return None

def save_data_to_db(data):
    if data:
        result = collection.insert_many(data)
        if result:
            print(f"Inserted {len(result.inserted_ids)} records into the database")
        else:
            print("Failed to insert data into the database")
    else:
        print("No data to insert")

def main():
    api_url = "https://api.example.com/data"
    data = fetch_external_data(api_url)
    save_data_to_db(data)

if __name__ == "__main__":
    main()
