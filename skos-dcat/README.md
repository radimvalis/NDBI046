# Assignment 4 - SKOS & DCAT-AP

### Instalace balíčků

Pro úspěšné spuštění všech skriptů je nutné nejprve nainstalovat potřebné balíčky:
```
pip install -r requirements.txt
```

### SKOS hierarchie

Slovník územních jednotek České republiky lze vygenerovat následujícím příkazem:
```
python3 skos-hierarchy.py > hierarchy.ttl
```

### DCAT dataset

DCAT dataset se generuje tímto příkazem:
```
python3 dataset-population.py > dataset-population.ttl
```