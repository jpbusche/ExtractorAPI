#!/bin/sh
echo "Trying connect to Elasticsearch"
until curl --output /dev/null --silent --head --fail http://elastic:9200 
do
	echo "Trying connect to Elasticsearch"
    sleep 30
done
echo "Connected with Elasticsearch"
curl -X PUT "elastic:9200/steam_tmp" -H 'Content-Type: application/json' -d'
{
    "mappings" : {
        "game_tmp" : {
            "properties" : {
                "price": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "double" }
					}},
				"userscore": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "double" }
					}},
				"currency": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"median_hours_played": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"owners": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"view_count": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"like_count": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"dislike_count": { "type": "nested",
					"properties": {
						"date": { "type": "date" },
						"value": { "type": "long" }
					}},
				"is_free": { "type": "boolean" }
            }
        }
    }
}
'
cd src/
celery -A schedule worker -B