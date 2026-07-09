#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "======================================"
echo " BIG DATA SIMULATION PIPELINE"
echo "======================================"

echo ""
echo "[1/5] Starting Hadoop cluster..."
docker compose up -d
echo "Waiting for NameNode to be ready..."
until docker compose exec namenode hdfs dfsadmin -report 2>/dev/null | grep -q "Live datanodes"; do
  echo "  Waiting..."
  sleep 5
done
echo "  NameNode is ready!"
echo "  Datanodes:"
docker compose exec namenode hdfs dfsadmin -report 2>/dev/null | grep -E "^(Name:|Hostname|Configured Capacity|DFS Used)"

echo ""
echo "[2/5] Generating big data (~1.5 GB total)..."
mkdir -p data
docker compose exec namenode python3 /scripts/generate_data.py

echo ""
echo "[3/5] Loading data into HDFS..."
docker compose exec namenode bash /scripts/load_to_hdfs.sh

echo ""
echo "[4/5] Verifying data in HDFS..."
docker compose exec namenode bash /scripts/verify_hdfs.sh

echo ""
echo "[5/5] Running sample analytics..."
docker compose exec namenode bash /scripts/run_analytics.sh

echo ""
echo "======================================"
echo " PIPELINE COMPLETE"
echo "======================================"
echo ""
echo "Web UIs:"
echo "  HDFS NameNode: http://localhost:9870"
echo "  YARN ResourceManager: http://localhost:8088"
echo ""
echo "To explore manually:"
echo "  docker compose exec namenode hdfs dfs -ls /user/root/bigdata-sim/transactions/"
echo "  docker compose exec namenode hdfs dfs -text /user/root/bigdata-sim/transactions/transactions.csv | head -5"
