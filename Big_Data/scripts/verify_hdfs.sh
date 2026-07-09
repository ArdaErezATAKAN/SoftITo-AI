#!/bin/bash
set -e

HDFS_BASE="/user/root/bigdata-sim"

echo "=== HDFS Directory Structure ==="
hdfs dfs -ls -R "${HDFS_BASE}" 2>/dev/null | head -20

echo ""
echo "=== File Sizes ==="
hdfs dfs -du -h "${HDFS_BASE}"

echo ""
echo "=== Block Report ==="
hdfs fsck "${HDFS_BASE}" -files -blocks -locations 2>/dev/null | head -30

echo ""
echo "=== HDFS Health ==="
hdfs dfsadmin -report 2>/dev/null | grep -E "^(Name:|Hostname|Configured Capacity|DFS Used|Non DFS Used|DFS Remaining|Live|Dead|Decommission)"

echo ""
echo "=== Sample Data (first 5 rows) ==="
echo "--- transactions ---"
hdfs dfs -text "${HDFS_BASE}/transactions/transactions.csv" 2>/dev/null | head -5
echo ""
echo "--- clickstream ---"
hdfs dfs -text "${HDFS_BASE}/clickstream/clickstream.log" 2>/dev/null | head -5
echo ""
echo "--- sensors ---"
hdfs dfs -text "${HDFS_BASE}/sensors/sensors.csv" 2>/dev/null | head -5
