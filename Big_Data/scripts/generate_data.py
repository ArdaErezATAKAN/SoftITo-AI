import csv
import random
import string
import time
import os
import sys
from datetime import datetime, timedelta

random.seed(42)

OUTPUT_DIR = "/Users/d1-07/bigdata-simulation/data"
ROWS_TOTAL = {
    "transactions": 5_000_000,
    "clickstream":  10_000_000,
    "sensors":      2_000_000,
}

PRODUCT_IDS = [f"PROD-{i:06d}" for i in range(1, 10001)]
USER_IDS = [f"USER-{i:06d}" for i in range(1, 100001)]
CITIES = ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa", "Adana", "Gaziantep", "Konya", "Mersin", "Diyarbakir"]
CATEGORIES = ["Electronics", "Clothing", "Food", "Books", "Home", "Sports", "Toys", "Health", "Automotive", "Music"]
PAYMENT_TYPES = ["CreditCard", "DebitCard", "BankTransfer", "MobilePay", "Cryptocurrency"]
PAGES = ["/home", "/products", "/cart", "/checkout", "/account", "/search", "/help", "/about", "/contact", "/blog"]
DEVICES = ["Mobile", "Desktop", "Tablet"]
SENSOR_TYPES = ["temperature", "humidity", "pressure", "wind_speed", "air_quality"]

BASE_TIME = datetime(2025, 1, 1)

def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_transactions(filename, count):
    print(f"Generating {count:,} transactions -> {filename}")
    t0 = time.time()
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["transaction_id", "user_id", "product_id", "category",
                         "amount", "quantity", "city", "payment_type",
                         "timestamp", "is_fraud"])
        for i in range(count):
            tid = f"TXN-{i+1:010d}"
            uid = random.choice(USER_IDS)
            pid = random.choice(PRODUCT_IDS)
            cat = random.choice(CATEGORIES)
            amount = round(random.uniform(5, 5000), 2)
            qty = random.randint(1, 10)
            city = random.choice(CITIES)
            pmt = random.choice(PAYMENT_TYPES)
            ts = random_date(BASE_TIME, BASE_TIME + timedelta(days=365))
            fraud = 1 if random.random() < 0.02 else 0
            writer.writerow([tid, uid, pid, cat, amount, qty, city, pmt,
                             ts.strftime("%Y-%m-%d %H:%M:%S"), fraud])
            if (i + 1) % 100000 == 0:
                elapsed = time.time() - t0
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                print(f"  Progress: {i+1:,}/{count:,} ({100*(i+1)/count:.0f}%) - {rate:,.0f} rows/s")
    print(f"  Done in {time.time()-t0:.1f}s, file size: {os.path.getsize(filename)/1024/1024:.1f} MB")

def generate_clickstream(filename, count):
    print(f"Generating {count:,} clickstream records -> {filename}")
    t0 = time.time()
    with open(filename, "w") as f:
        f.write("session_id|user_id|page|action|device|ip_address|timestamp|duration_sec\n")
        for i in range(count):
            sid = f"SESS-{random.randint(1, 500000):08d}"
            uid = random.choice(USER_IDS) if random.random() < 0.7 else "guest"
            page = random.choice(PAGES)
            action = random.choice(["view", "click", "scroll", "submit", "exit"])
            dev = random.choice(DEVICES)
            ip = f"{random.randint(10, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            ts = random_date(BASE_TIME, BASE_TIME + timedelta(days=365))
            dur = random.randint(1, 600)
            f.write(f"{sid}|{uid}|{page}|{action}|{dev}|{ip}|{ts.strftime('%Y-%m-%d %H:%M:%S')}|{dur}\n")
            if (i + 1) % 200000 == 0:
                elapsed = time.time() - t0
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                print(f"  Progress: {i+1:,}/{count:,} ({100*(i+1)/count:.0f}%) - {rate:,.0f} rows/s")
    print(f"  Done in {time.time()-t0:.1f}s, file size: {os.path.getsize(filename)/1024/1024:.1f} MB")

def generate_sensors(filename, count):
    print(f"Generating {count:,} sensor readings -> {filename}")
    t0 = time.time()
    with open(filename, "w") as f:
        f.write("sensor_id,timestamp,sensor_type,value,unit,location,status\n")
        for i in range(count):
            sid = f"SENSOR-{random.randint(1, 5000):05d}"
            stype = random.choice(SENSOR_TYPES)
            ts = random_date(BASE_TIME, BASE_TIME + timedelta(days=90))
            if stype == "temperature":
                val = round(random.gauss(25, 10), 2)
                unit = "C"
            elif stype == "humidity":
                val = round(random.gauss(60, 20), 1)
                unit = "%"
            elif stype == "pressure":
                val = round(random.gauss(1013, 20), 1)
                unit = "hPa"
            elif stype == "wind_speed":
                val = round(random.gauss(12, 8), 1)
                unit = "km/h"
            else:
                val = round(random.gauss(50, 25), 0)
                unit = "AQI"
            loc = random.choice(CITIES)
            status = random.choice(["active", "active", "active", "warning", "error"])
            f.write(f"{sid},{ts.strftime('%Y-%m-%d %H:%M:%S')},{stype},{val},{unit},{loc},{status}\n")
            if (i + 1) % 100000 == 0:
                elapsed = time.time() - t0
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                print(f"  Progress: {i+1:,}/{count:,} ({100*(i+1)/count:.0f}%) - {rate:,.0f} rows/s")
    print(f"  Done in {time.time()-t0:.1f}s, file size: {os.path.getsize(filename)/1024/1024:.1f} MB")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_transactions(os.path.join(OUTPUT_DIR, "transactions.csv"), ROWS_TOTAL["transactions"])
    generate_clickstream(os.path.join(OUTPUT_DIR, "clickstream.log"), ROWS_TOTAL["clickstream"])
    generate_sensors(os.path.join(OUTPUT_DIR, "sensors.csv"), ROWS_TOTAL["sensors"])

    print("\n=== SUMMARY ===")
    for fname in ["transactions.csv", "clickstream.log", "sensors.csv"]:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(fpath):
            size_mb = os.path.getsize(fpath) / 1024 / 1024
            print(f"  {fname}: {size_mb:.1f} MB")
