# fakeapp-radar-db

Base de datos PostgreSQL de FakeApp Radar (corre en Docker).

## Levantar
1. Copia `.env.example` a `.env` y pon una contraseña real.
2. `docker compose up -d`
3. Revisa el estado con `docker compose ps` (debe decir "healthy").

## Notas
- Solo escucha en 127.0.0.1 (tu propia computadora), no en la red.
- Los scripts de `init/` se ejecutan una sola vez, al crear el volumen.
- Las migraciones del esquema viven en el repo `fakeapp-radar-api` (Alembic).