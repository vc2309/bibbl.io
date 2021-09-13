docker-compose up&
sleep 5
pytest tests/unit
docker-compose down
