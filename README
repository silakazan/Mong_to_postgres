+------------------+        +-----------------+        +------------------+
|   shipments      |        |    parcels      |        |    addresses     |
+------------------+        +-----------------+        +------------------+
| shipment_id (PK) |◄──────►| parcel_id (PK)  |        | address_id (PK)  |
| date             |        | shipment_id (FK)|◄──────►| shipment_id (FK) |
+------------------+        | barcode         |        | street           |
                           +-----------------+        | city             |
                                                     | zip_code         |
                                                     +------------------+

Kodda üç ana tablo bulunmaktadır:

shipments
parcels
addresses
Ve bunlar arasında aşağıdaki ilişkiler vardır:

İlişkiler:
shipments tablosundaki her bir sevkiyat (shipment_id), parcels ve addresses tablolarındaki ilgili verilerle ilişkilidir.
parcels tablosundaki her bir paket (parcel_id) bir shipment_id ile bağlanır, bu da shipments tablosundaki bir sevkiyata işaret eder.
addresses tablosundaki her bir adres (address_id) de bir shipment_id ile bağlanır, bu da ilgili sevkiyatı işaret eder.

Açıklamalar:
shipments tablosundaki shipment_id birincil anahtar (PK) olarak kullanılır ve parcels ve addresses tablolarındaki shipment_id alanları, sırasıyla bu tablolarda dış anahtar (FK) olarak kullanılır.
parcels tablosundaki parcel_id birincil anahtar (PK) olup her paketi benzersiz bir şekilde tanımlar.
addresses tablosundaki address_id birincil anahtar (PK) olup her adresi benzersiz bir şekilde tanımlanır.
