#!/usr/bin/env python3
"""
BIG DATA SIMULASYONU
====================
HDFS + Hadoop ekosistemi üzerinde çalışan,
17 milyon kayıtlı (~1.4 GB) rastgele veri üretimi ve analizi.
"""

import csv
import os
import random
import string
import subprocess
import sys
import time
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# 1. KONFIGÜRASYON
# ============================================================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")

ROWS_TOTAL = {
    "transactions": 5_000_000,
    "clickstream": 10_000_000,
    "sensors": 2_000_000,
}

PRODUCT_IDS = [f"PROD-{i:06d}" for i in range(1, 10001)]
USER_IDS = [f"USER-{i:06d}" for i in range(1, 100001)]
CITIES = ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa",
          "Adana", "Gaziantep", "Konya", "Mersin", "Diyarbakir"]
CATEGORIES = ["Electronics", "Clothing", "Food", "Books", "Home",
              "Sports", "Toys", "Health", "Automotive", "Music"]
PAYMENT_TYPES = ["CreditCard", "DebitCard", "BankTransfer", "MobilePay", "Cryptocurrency"]
PAGES = ["/home", "/products", "/cart", "/checkout", "/account",
         "/search", "/help", "/about", "/contact", "/blog"]
DEVICES = ["Mobile", "Desktop", "Tablet"]
SENSOR_TYPES = ["temperature", "humidity", "pressure", "wind_speed", "air_quality"]

BASE_TIME = datetime(2025, 1, 1)

# ============================================================
# 2. VERİ ÜRETİCİ
# ============================================================
def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_transactions(filename, count):
    print(f"[1/3] {count:,} transaction üretiliyor...")
    t0 = time.time()
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["transaction_id", "user_id", "product_id", "category",
                         "amount", "quantity", "city", "payment_type",
                         "timestamp", "is_fraud"])
        for i in range(count):
            writer.writerow([
                f"TXN-{i+1:010d}",
                random.choice(USER_IDS),
                random.choice(PRODUCT_IDS),
                random.choice(CATEGORIES),
                round(random.uniform(5, 5000), 2),
                random.randint(1, 10),
                random.choice(CITIES),
                random.choice(PAYMENT_TYPES),
                random_date(BASE_TIME, BASE_TIME + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S"),
                1 if random.random() < 0.02 else 0
            ])
            if (i + 1) % 1_000_000 == 0:
                print(f"   {i+1:,}/{count:,} ({100*(i+1)//count}%)")
    print(f"   Bitti: {time.time()-t0:.1f}s, {os.path.getsize(filename)/1024/1024:.1f} MB")

def generate_clickstream(filename, count):
    print(f"[2/3] {count:,} clickstream kaydı üretiliyor...")
    t0 = time.time()
    with open(filename, "w") as f:
        f.write("session_id|user_id|page|action|device|ip_address|timestamp|duration_sec\n")
        for i in range(count):
            f.write(
                f"SESS-{random.randint(1, 500000):08d}|"
                f"{random.choice(USER_IDS) if random.random() < 0.7 else 'guest'}|"
                f"{random.choice(PAGES)}|"
                f"{random.choice(['view','click','scroll','submit','exit'])}|"
                f"{random.choice(DEVICES)}|"
                f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}|"
                f"{random_date(BASE_TIME, BASE_TIME + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')}|"
                f"{random.randint(1, 600)}\n"
            )
            if (i + 1) % 2_000_000 == 0:
                print(f"   {i+1:,}/{count:,} ({100*(i+1)//count}%)")
    print(f"   Bitti: {time.time()-t0:.1f}s, {os.path.getsize(filename)/1024/1024:.1f} MB")

def generate_sensors(filename, count):
    print(f"[3/3] {count:,} sensor okuması üretiliyor...")
    t0 = time.time()
    with open(filename, "w") as f:
        f.write("sensor_id,timestamp,sensor_type,value,unit,location,status\n")
        for i in range(count):
            stype = random.choice(SENSOR_TYPES)
            ts = random_date(BASE_TIME, BASE_TIME + timedelta(days=90))
            if stype == "temperature":
                val, unit = round(random.gauss(25, 10), 2), "C"
            elif stype == "humidity":
                val, unit = round(random.gauss(60, 20), 1), "%"
            elif stype == "pressure":
                val, unit = round(random.gauss(1013, 20), 1), "hPa"
            elif stype == "wind_speed":
                val, unit = round(random.gauss(12, 8), 1), "km/h"
            else:
                val, unit = round(random.gauss(50, 25), 0), "AQI"
            f.write(
                f"SENSOR-{random.randint(1, 5000):05d},"
                f"{ts.strftime('%Y-%m-%d %H:%M:%S')},{stype},{val},{unit},"
                f"{random.choice(CITIES)},"
                f"{random.choice(['active','active','active','warning','error'])}\n"
            )
            if (i + 1) % 500_000 == 0:
                print(f"   {i+1:,}/{count:,} ({100*(i+1)//count}%)")
    print(f"   Bitti: {time.time()-t0:.1f}s, {os.path.getsize(filename)/1024/1024:.1f} MB")

def generate_all_data():
    print("\n=== VERİ ÜRETİMİ ===")
    os.makedirs(DATA_DIR, exist_ok=True)
    generate_transactions(os.path.join(DATA_DIR, "transactions.csv"), ROWS_TOTAL["transactions"])
    generate_clickstream(os.path.join(DATA_DIR, "clickstream.log"), ROWS_TOTAL["clickstream"])
    generate_sensors(os.path.join(DATA_DIR, "sensors.csv"), ROWS_TOTAL["sensors"])
    total_mb = sum(
        os.path.getsize(os.path.join(DATA_DIR, f)) / 1024 / 1024
        for f in ["transactions.csv", "clickstream.log", "sensors.csv"]
    )
    print(f"\nToplam: {total_mb:.1f} MB veri üretildi.\n")

# ============================================================
# 3. DOCKER / HDFS YÖNETİMİ
# ============================================================
def run(cmd, capture=False, cwd=None):
    """Kabuk komutu çalıştır."""
    kwargs = {"shell": True, "cwd": cwd or PROJECT_DIR}
    if capture:
        kwargs.update({"capture_output": True, "text": True})
    return subprocess.run(cmd, **kwargs)

def cluster_start():
    print("\n=== HADOOP CLUSTER BAŞLATILIYOR ===")
    run("docker compose up -d", cwd=PROJECT_DIR)
    print("NameNode hazır olana kadar bekleniyor...")
    for _ in range(30):
        result = run('docker compose exec namenode hdfs dfsadmin -report 2>/dev/null | grep -c "Live datanodes"', capture=True)
        if result.stdout and int(result.stdout.strip()) > 0:
            print("Cluster hazır!\n")
            return True
        time.sleep(5)
    print("HATA: Cluster zamanında hazır olmadı!")
    return False

def cluster_stop():
    print("\n=== CLUSTER DURDURULUYOR ===")
    run("docker compose down", cwd=PROJECT_DIR)
    print("Cluster durduruldu.\n")

def load_to_hdfs():
    print("\n=== HDFS'E VERİ YÜKLENİYOR ===")
    HDFS_BASE = "/user/root/bigdata-sim"
    files = [
        ("transactions", "transactions.csv"),
        ("clickstream", "clickstream.log"),
        ("sensors", "sensors.csv"),
    ]
    for folder, filename in files:
        run(f'docker compose exec namenode hdfs dfs -mkdir -p "{HDFS_BASE}/{folder}"', cwd=PROJECT_DIR)
        run(f'docker compose exec namenode hdfs dfs -put -f "/data/{filename}" "{HDFS_BASE}/{folder}/"', cwd=PROJECT_DIR)
        result = run(f'docker compose exec namenode hdfs dfs -ls "{HDFS_BASE}/{folder}/"', cwd=PROJECT_DIR, capture=True)
        print(result.stdout.strip())
    print("HDFS'e yükleme tamam.\n")

# ============================================================
# 4. ANALİTİK
# ============================================================
def run_namenode(cmd, capture=False):
    """Namenode container içinde komut çalıştır."""
    full_cmd = f'docker compose exec -T namenode bash -c {sh_quote(cmd)}'
    return run(full_cmd, capture=capture)

def sh_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def run_analytics():
    print("================" * 4)
    print(" HDFS VERİ ANALİZİ")
    print("================" * 4)

    HDFS_BASE = "/user/root/bigdata-sim"

    queries = [
        ("En aktif 5 şehir (işlem sayısı)",
         f'hdfs dfs -cat {HDFS_BASE}/transactions/transactions.csv 2>/dev/null | '
         f'awk -F, \'NR>1 {{print $7}}\' | sort | uniq -c | sort -rn | head -5'),

        ("En çok gelir getiren 5 kategori",
         f'hdfs dfs -cat {HDFS_BASE}/transactions/transactions.csv 2>/dev/null | '
         f'awk -F, \'NR>1 {{cat=$4; amt=$5; qty=$6; rev=amt*qty; cats[cat]+=rev}} '
         f'END {{for(c in cats) printf "%s: %.2f\\n",c,cats[c]}}\' | sort -t: -k2 -rn | head -5'),

        ("Şehirlere göre fraud oranı (top 5)",
         f'hdfs dfs -cat {HDFS_BASE}/transactions/transactions.csv 2>/dev/null | '
         f'awk -F, \'NR>1 {{city=$7; fraud=$10; total[city]++; frauds[city]+=fraud}} '
         f'END {{for(c in total) printf "%s: %%.2f (%d/%d)\\n",c,(frauds[c]/total[c])*100,frauds[c],total[c]}}\' '
         f'| sort -t: -k2 -rn | head -5'),

        ("En çok ziyaret edilen 5 sayfa",
         f'hdfs dfs -cat {HDFS_BASE}/clickstream/clickstream.log 2>/dev/null | '
         f'awk -F"|" \'NR>1 {{pages[$3]++}} END {{for(p in pages) print pages[p],p}}\' | sort -rn | head -5'),

        ("Cihaz dağılımı",
         f'hdfs dfs -cat {HDFS_BASE}/clickstream/clickstream.log 2>/dev/null | '
         f'awk -F"|" \'NR>1 {{dev[$5]++}} END {{for(d in dev) printf "%s: %d (%%.1f%%)\\n",d,dev[d],dev[d]/NR*100}}\' '
         f'| sort -t: -k2 -rn'),

        ("Sensör ortalamaları",
         f'hdfs dfs -cat {HDFS_BASE}/sensors/sensors.csv 2>/dev/null | '
         f'awk -F, \'NR>1 {{stype=$3; val=$4; count[stype]++; sum[stype]+=val}} '
         f'END {{for(s in count) printf "%s: ortalama=%%.2f (n=%d)\\n",s,sum[s]/count[s],count[s]}}\' '
         f'| sort -t: -k1'),

        ("HDFS Depolama", f'hdfs dfs -du -h {HDFS_BASE}'),
    ]

    for title, query in queries:
        print(f"\n>>> {title}")
        result = run_namenode(query, capture=True)
        output = result.stdout.strip() if result.stdout else ""
        print(output if output else "(sonuç yok)")

    print("\n================" * 4 + "\n")

# ============================================================
# 5. ANA PİPLİNE
# ============================================================
def main():
    print("=" * 50)
    print("  BIG DATA SIMULASYONU")
    print("  Hadoop + HDFS + 17M kayıt (~1.4 GB)")
    print("=" * 50)

    step = 1
    steps = [
        ("Cluster başlatma", cluster_start),
        ("Veri üretimi", generate_all_data),
        ("HDFS'e yükleme", load_to_hdfs),
        ("Analitik sorgular", run_analytics),
    ]

    for name, func in steps:
        print(f"\nAdım {step}/{len(steps)}: {name}")
        func()
        step += 1

    print("\n" + "=" * 50)
    print("  PİPLİNE TAMAMLANDI")
    print("  Web UI: http://localhost:9870 (HDFS)")
    print("  Web UI: http://localhost:8088 (YARN)")
    print("=" * 50)


if __name__ == "__main__":
    main()
