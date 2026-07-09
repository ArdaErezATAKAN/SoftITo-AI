# Data Klasörü
Bu klasör, `bigdata_simulation.py` çalıştırıldığında otomatik olarak 
oluşturulan veri dosyalarını içerir:

- `transactions.csv` (~470MB)
- `clickstream.log` (~795MB)
- `sensors.csv` (~128MB)

Boyut sınırı nedeniyle bu dosyalar repoda barındırılmamaktadır.
Script `random.seed(42)` kullandığından, çalıştıran herkes birebir 
aynı veri setini elde eder (deterministik üretim).
