# Assignment 2 - Apache Airflow

### Obsah adresáře

Všechny důležité soubory se nacházejí v adresáři `dags/`. DAG generující datové kostky je definován v souboru `dag_data_cubes.py`. Jeho operátory využívají skripty uložené v adresáři `dags/scripts/`. Po spuštění workflow se v adresáři objeví adresáře `dags/inputs/`, kam se stahují zdrojové CSV soubory a `dags/outputs/`, kde se po skončení procesu objeví výsledné datové kostky - soubory `health_care.ttl` a `population.ttl`.

### Spuštění

Vytvoření a spuštění Docker kontejneru lze provést následujícími příkazy:
```
cd ~/NDBI046/airflow
docker compose up --build
```

Po nastartování kontejneru je webserver dostupný na adrese: [http://localhost:8080](http://localhost:8080). Přihlašovací jméno je `airflow`, heslo je také `airflow`.

Zastavit a odstranit kontejner lze tímto příkazem:
```
docker compose down --volumes --rmi all
```