docker-compose up&
sleep 5
pytest tests/unit -vrP
docker-compose down
