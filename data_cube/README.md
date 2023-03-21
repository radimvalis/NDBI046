# Assignment 1 - Data Cube


## Získání zdrojových dat

V adresáři `~/NDBI046/data_cube` spusťte program `download_data.sh`, který stáhne potřebná data:
```
cd ~/NDBI046/data_cube
bash download_data.sh
```
V adresáři `~/NDBI046/data_cube` by se měly objevit soubory `population-2021.csv`, `health-care.csv` a `lau-nuts-mapping.csv`.

Zdrojová data a další informace jsou dostupné následujících odkazech:

* [population-2021.csv](https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F12032e1445fd74fa08da79b14137fc29)
* [health-care.csv](https://data.gov.cz/datov%C3%A1-sada?iri=https://data.gov.cz/zdroj/datov%C3%A9-sady/https---opendata.mzcr.cz-api-3-action-package_show-id-nrpzs)
* [lau-nuts-mapping.csv](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/%C4%8D%C3%ADseln%C3%ADk-okres%C5%AF-vazba-101-nad%C5%99%C3%ADzen%C3%BD.csv)


## Instalace závislostí

Vytvořte virtuální prostředí a nainstalujte potřebné balíčky:
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Obsah adresáře

Pro generování datových kostek slouží skripty `population.py` a `health_care.py`. Oba skripty využívají společný interface, definovaný v souboru `datacube.py`. Zdrojová data pro datové kostky jsou po spuštění skriptu `download_data.sh` uložena v souborech `population-2021.csv`, `health-care.csv` a `lau-nuts-mapping.csv`. Skript `datacube_validation.py` validuje vytvořené datové kostky pomocí dotazů, uložených v souboru `validation_queries.sparql`.


### Generování datových kostek

Datovou kostku mapující populaci České republiky lze vytvořit následujícím příkazem:
```
python population.py population-2021.csv > datacube-population-2021.ttl
```
Výsledek bude uložen v souboru `datacube-population-2021.ttl` ve formátu Turtle.

Datová kostka shrnující zdravotní péči v České republice se vygeneruje tímto příkazem:
```
python health_care.py health-care.csv > datacube-health-care.ttl
```
Výsledek bude uložen v souboru `datacube-health-care.ttl`, opět ve formátu Turtle.


### Validace datových kostek

Validace datových kostek probíhá na základě [integritních omezení](https://www.w3.org/TR/vocab-data-cube/#wf-rules), která se spouší prostřednictvím skriptu `datacube_validation.py`.

Validace souboru `datacube-health-care.ttl`:
```
python datacube_validation.py datacube-health-care.ttl 
```

Validace souboru `datacube-population-2021.ttl`:
```
python datacube_validation.py datacube-population-2021.ttl
```

*Poznámky:*
* *Třetí integritní omezení (IC-3) neprochází testem, jelikož se v dotazu používá obecná `qb:componentProperty`, datová kostka ale používá jejího specializovaného potomka - `qb:measure`.*
* *Sedmé integritní omezení (IC-7) se nedaří vyhodnotit, zřejmě kvůli chybě v balíčku [rdflib](https://rdflib.readthedocs.io/en/stable/index.html).*