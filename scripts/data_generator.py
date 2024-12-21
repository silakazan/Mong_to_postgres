from pymongo import MongoClient
import random
from datetime import datetime, timezone

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017")
db = client.mydatabase
collection = db.mycollection
#db = client["shipments"]
#collection = db["shipment_data"]

# Veri oluşturucu
def generate_data():
    for _ in range(10):  # 10 sevkiyat
        shipment = {
            "shipment_id": f"SHIP{random.randint(1000, 9999)}",
            "date": datetime.now(timezone.utc),
            "parcels": [f"PARCEL{random.randint(100, 999)}" for _ in range(5)],
            "barcodes": [f"BARCODE{random.randint(1000, 9999)}" for _ in range(5)],
            "address": {
                "street": f"Street {random.randint(1, 100)}",
                "city": "Istanbul",
                "zip_code": f"{random.randint(10000, 99999)}",
            },
        }
        collection.insert_one(shipment)
    print("Veri MongoDB'ye başarıyla eklendi.")
    
# Veriyi MongoDB'den okuma ve yazdırma
def print_data():
    shipments = collection.find()  # Tüm verileri al
    for shipment in shipments:
        print(shipment)


if __name__ == "__main__":
    generate_data()
    print_data()
