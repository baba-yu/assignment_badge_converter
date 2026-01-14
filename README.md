# assignment_badge_converter
## DB
Launch postgres docker container.
```
sudo docker compose -f assignment_badge_converter_infra/docker-compose.yml up -d db
```

Check database
```
psql -h 127.0.0.1 -p 5435 -U app -d app
```

## Backend
You have to create venv before launching backend server. 
```
cd assignment_badge_converter_backend
source .venv/bin/activate
python manage.py migrate
python manage.py runserver 0.0.0.0:8081

```

## Frontend
```
docker compose -f assignment_badge_converter_infra/docker-compose.yml up frontend
```