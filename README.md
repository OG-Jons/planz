# Planz

Planz is a web application for plant care and management. It allows users to track the statistics of their plants. Other than the application itself, you also need to build your own sensors

## Sensor Setup
For each plant, you need to set up a sensor. The sensor is a small device that measures the temperature and humidity of the plant. It is connected to the internet and sends the data to the server.

For the sensor, you can follow the guide here: [docs/sensor.md](./docs/sensor.md)

## Deployment

### Docker Compose

To run planz on your server or local machine, you can use Docker Compose. This is the recommended way to run planz.
With the help of Docker Compose, you can run planz in a single file and command.
```yaml
services:
  postgres:
    image: postgres:17-alpine
    environment:
      - POSTGRES_USER=fastapi
      - POSTGRES_PASSWORD=secret # Change this to a strong password
      - POSTGRES_DB=plantsdb
    networks:
      - app_network
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fastapi -d plantsdb"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    image: ghcr.io/og-jons/planz:latest
    volumes:
      - media:/app/media
    ports:
      - "8080:8000" # Define the port you want to use, by changing 8080
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - POSTGRES_USER=fastapi
      - POSTGRES_PASSWORD=secret # Change this to the same password as above
      - POSTGRES_DB=plantsdb
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
    networks:
      - app_network

volumes:
  postgres_data:
  media:

networks:
  app_network:
    driver: bridge
```

## Backend Development

Backend docs: [docs/backend.md](./docs/backend.md).

## Frontend Development

Frontend docs: [docs/frontend.md](./docs/frontend.md).


## Development

TBD

[//]: # (General development docs: [development.md]&#40;./development.md&#41;.)