"""Carga los archivos de seeds/*.sql en orden. Se puede correr varias veces (los seeds usan ON CONFLICT)."""
import os
from pathlib import Path

import psycopg


def main() -> None:
    seeds_dir = Path(os.environ.get("SEEDS_DIR", "seeds"))
    files = sorted(seeds_dir.glob("*.sql"))
    with psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    ) as conn:  # confirma al salir; si algo falla, revierte todo
        for f in files:
            conn.execute(f.read_text(encoding="utf-8"))
            print(f"Seed aplicado: {f.name}")
    print(f"Listo: {len(files)} seed(s).")


if __name__ == "__main__":
    main()
