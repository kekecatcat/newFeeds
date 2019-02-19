#!/bin/bash

#redis-server --daemonize yes
redis-server > /tmp/redis.log &
predis_pid=$!

mongod > /tmp/mongo.log &
pmongo_pid=$!


pip3 install -r requirements.txt

cd news_pipeline
python3 news_monitor.py &
p1_pid=$!
python3 news_fetcher.py &
p2_pid=$!
python3 news_deduper.py &
p3_pid=$!

echo "================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESS." PRESSKEY

kill $p1_pid $p2_pid $p3_pid $predis_pid $pmongo_pid