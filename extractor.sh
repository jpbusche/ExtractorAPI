#!/bin/sh
echo "Trying connect to Elasticsearch"
until curl --output /dev/null --silent --head --fail http://elastic:9200 
do
	echo "Trying connect to Elasticsearch"
    sleep 5
done
echo "Connected with Elasticsearch"
python src/main.py