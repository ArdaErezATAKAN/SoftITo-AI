#!/bin/bash
set -e

HDFS_USER="${HDFS_USER:-root}"
DATA_DIR="/data"
HDFS_BASE="/user/${HDFS_USER}/bigdata-sim"

echo "=== Creating HDFS directories ==="
hdfs dfs -mkdir -p "${HDFS_BASE}/transactions"
hdfs dfs -mkdir -p "${HDFS_BASE}/clickstream"
hdfs dfs -mkdir -p "${HDFS_BASE}/sensors"

echo "=== Loading transactions.csv to HDFS ==="
hdfs dfs -put -f "${DATA_DIR}/transactions.csv" "${HDFS_BASE}/transactions/"
hdfs dfs -ls "${HDFS_BASE}/transactions/"

echo "=== Loading clickstream.log to HDFS ==="
hdfs dfs -put -f "${DATA_DIR}/clickstream.log" "${HDFS_BASE}/clickstream/"
hdfs dfs -ls "${HDFS_BASE}/clickstream/"

echo "=== Loading sensors.csv to HDFS ==="
hdfs dfs -put -f "${DATA_DIR}/sensors.csv" "${HDFS_BASE}/sensors/"
hdfs dfs -ls "${HDFS_BASE}/sensors/"

echo ""
echo "=== HDFS Storage Summary ==="
hdfs dfs -du -h "${HDFS_BASE}"
