from pymongo import MongoClient
import psycopg2
from psycopg2 import extensions
from pytz import timezone
from datetime import datetime

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017")
db = client["shipments"]
collection = db["shipment_data"]

# PostgreSQL veritabanını oluşturma
def create_new_database():
    try:
        # PostgreSQL'e bağlan
        temp_conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        temp_conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        temp_cursor = temp_conn.cursor()

        # Yeni veritabanını oluştur
        temp_cursor.execute("CREATE DATABASE shipments_3;")
        print("Yeni veritabanı 'shipments_3' oluşturuldu.")
        
        temp_cursor.close()
        temp_conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print("Veritabanı 'shipments_3' zaten mevcut, yeniden oluşturulmadı.")
    except Exception as e:
        print(f"Yeni veritabanı oluşturulurken bir hata oluştu: {e}")

# PostgreSQL bağlantısı ve tablo oluşturma
def setup_tables():
    try:
        conn = psycopg2.connect(
            dbname="shipments_3",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        print("PostgreSQL bağlantısı başarılı")

        # PostgreSQL tablolarını oluştur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            shipment_id VARCHAR PRIMARY KEY,
            date TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS parcels (
            parcel_id SERIAL PRIMARY KEY,
            shipment_id VARCHAR NOT NULL,
            barcode VARCHAR UNIQUE,  -- Barcode'a UNIQUE constraint ekleyin
            FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
        );
        CREATE TABLE IF NOT EXISTS addresses (
            address_id SERIAL PRIMARY KEY,
            shipment_id VARCHAR NOT NULL,
            street VARCHAR,
            city VARCHAR,
            zip_code VARCHAR,
            FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
        );
        """)
        conn.commit()
        print("Tablolar başarıyla oluşturuldu.")
        return conn, cursor
    except psycopg2.OperationalError as e:
        print(f"PostgreSQL bağlantısı sırasında bir hata oluştu: {e}")
        raise

# Duplicate kontrolü için veritabanında sorgu yap
def check_duplicate(cursor, shipment_id, barcode=None):
    if barcode:
        cursor.execute("SELECT COUNT(*) FROM parcels WHERE barcode = %s", (barcode,))
        count = cursor.fetchone()[0]
        return count > 0  # Eğer duplicate varsa, True döndürür
    else:
        cursor.execute("SELECT COUNT(*) FROM shipments WHERE shipment_id = %s", (shipment_id,))
        count = cursor.fetchone()[0]
        return count > 0  # Eğer duplicate varsa, True döndürür

# Veri doğrulama
def validate_data(doc):
    # shipment_id'nin var olup olmadığını kontrol et
    if not doc.get("shipment_id"):
        raise ValueError("shipment_id eksik")
    
    # Tarih bilgisinin geçerli olup olmadığını kontrol et
    if not isinstance(doc.get("date"), datetime):
        raise ValueError("Geçersiz tarih formatı")
    
    # Adres bilgilerini doğrula
    if not doc.get("address") or not doc["address"].get("street"):
        raise ValueError("Adres bilgileri eksik")

    return True  # Eğer veriler geçerliyse True döndürür

# MongoDB’den PostgreSQL’e aktarım
def etl_process(cursor, conn):
    for doc in collection.find():
        try:
            if validate_data(doc):
                shipment_id = doc["shipment_id"]
                date = doc["date"].astimezone(timezone("Europe/Istanbul"))

                # Duplicate kontrolü
                if not check_duplicate(cursor, shipment_id):
                    # Sevkiyat bilgilerini ekle
                    cursor.execute(
                        "INSERT INTO shipments (shipment_id, date) VALUES (%s, %s)",
                        (shipment_id, date)
                    )
                else:
                    print(f"Duplicate shipment_id {shipment_id} bulundu, veri eklenmedi.")
                    continue

                # Paket bilgilerini ekle
                for barcode in doc["barcodes"]:
                    if not check_duplicate(cursor, shipment_id, barcode):
                        cursor.execute(
                            "INSERT INTO parcels (shipment_id, barcode) VALUES (%s, %s)",
                            (shipment_id, barcode)
                        )
                    else:
                        print(f"Duplicate barcode {barcode} bulundu, paket verisi eklenmedi.")
                
                # Adres bilgilerini ekle
                address = doc["address"]
                cursor.execute(
                    "INSERT INTO addresses (shipment_id, street, city, zip_code) VALUES (%s, %s, %s, %s)",
                    (shipment_id, address["street"], address["city"], address["zip_code"])
                )
        except ValueError as e:
            print(f"Veri doğrulama hatası: {e}")
        except Exception as e:
            print(f"Genel bir hata oluştu: {e}")

    conn.commit()
    print("Veri başarıyla PostgreSQL'e aktarıldı.")

# PostgreSQL verilerini görüntüleme
def print_postgresql_data(cursor):
    print("\n--- Sevkiyat Verileri ---")
    cursor.execute("SELECT * FROM shipments;")
    shipments = cursor.fetchall()
    for shipment in shipments:
        print(shipment)

    print("\n--- Paket Verileri ---")
    cursor.execute("SELECT * FROM parcels;")
    parcels = cursor.fetchall()
    for parcel in parcels:
        print(parcel)

    print("\n--- Adres Verileri ---")
    cursor.execute("SELECT * FROM addresses;")
    addresses = cursor.fetchall()
    for address in addresses:
        print(address)

if __name__ == "__main__":
    create_new_database()  # Yeni veritabanını oluştur
    conn, cursor = setup_tables()  # Yeni tabloları oluştur
    etl_process(cursor, conn)  # ETL işlemini başlat
    print_postgresql_data(cursor)  # PostgreSQL verilerini görüntüle
