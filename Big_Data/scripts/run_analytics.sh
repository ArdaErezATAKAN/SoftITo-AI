#!/bin/bash
set -e

HDFS_BASE="/user/root/bigdata-sim"

echo "============================================"
echo " SAMPLE ANALYTICS ON HDFS DATA"
echo "============================================"

echo ""
echo "1. Top 5 cities by transaction count:"
hdfs dfs -cat "${HDFS_BASE}/transactions/transactions.csv" 2>/dev/null | \
  awk -F',' 'NR>1 {print $7}' | sort | uniq -c | sort -rn | head -5

echo ""
echo "2. Top 5 categories by revenue:"
hdfs dfs -cat "${HDFS_BASE}/transactions/transactions.csv" 2>/dev/null | \
  awk -F',' 'NR>1 {cat=$4; amt=$5; qty=$6; rev=amt*qty; cats[cat]+=rev} END {for(c in cats) printf "%s: %.2f\n",c,cats[c]}' | \
  sort -t: -k2 -rn | head -5

echo ""
echo "3. Fraud rate by city:"
hdfs dfs -cat "${HDFS_BASE}/transactions/transactions.csv" 2>/dev/null | \
  awk -F',' 'NR>1 {city=$7; fraud=$10; total[city]++; frauds[city]+=fraud} END {for(c in total) printf "%s: %.2f%% (%d/%d)\n",c,(frauds[c]/total[c])*100,frauds[c],total[c]}' | \
  sort -t: -k2 -rn | head -5

echo ""
echo "4. Most visited pages (clickstream):"
hdfs dfs -cat "${HDFS_BASE}/clickstream/clickstream.log" 2>/dev/null | \
  awk -F'|' 'NR>1 {pages[$3]++} END {for(p in pages) print pages[p],p}' | \
  sort -rn | head -5

echo ""
echo "5. Device breakdown (clickstream):"
hdfs dfs -cat "${HDFS_BASE}/clickstream/clickstream.log" 2>/dev/null | \
  awk -F'|' 'NR>1 {dev[$5]++} END {for(d in dev) printf "%s: %d (%.1f%%)\n",d,dev[d],dev[d]/NR*100}' | \
  sort -t: -k2 -rn

echo ""
echo "6. Average sensor values by type:"
hdfs dfs -cat "${HDFS_BASE}/sensors/sensors.csv" 2>/dev/null | \
  awk -F',' 'NR>1 {stype=$3; val=$4; count[stype]++; sum[stype]+=val} END {for(s in count) printf "%s: avg=%.2f (n=%d)\n",s,sum[s]/count[s],count[s]}' | \
  sort -t: -k1

echo ""
echo "7. Total data size:"
hdfs dfs -du -h "${HDFS_BASE}"
echo ""

echo "============================================"
echo " ANALYTICS COMPLETE"
echo "============================================"
