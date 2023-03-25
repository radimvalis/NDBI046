import os, pendulum
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from scripts import download, health_care, population

URL_HEALTH_CARE = "https://opendata.mzcr.cz/data/nrpzs/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"
URL_POPULATION = "https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv"
URL_LAU_NUTS_MAP = "https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/%C4%8D%C3%ADseln%C3%ADk-okres%C5%AF-vazba-101-nad%C5%99%C3%ADzen%C3%BD.csv"

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DIR_INPUTS = DIR_PATH + "/inputs/"
DIR_OUTPUTS = DIR_PATH + "/outputs/"

CSV_HEALTH_CARE = DIR_INPUTS + "health-care.csv"
CSV_POPOPULATION = DIR_INPUTS + "population.csv"
CSV_LAU_NUTS_MAP = DIR_INPUTS +"lau-nuts-mapping.csv"

TTL_HEALTH_CARE = DIR_OUTPUTS + "health_care.ttl"
TTL_POPULATION = DIR_OUTPUTS + "population.ttl"

@dag(
    dag_id="data-cubes",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 25)
)

def create_datacubes():

    create_data_dirs = BashOperator(
        task_id="create_data_dirs",
        bash_command=f" [[ ! -d {DIR_INPUTS} ]] && mkdir {DIR_INPUTS} ; [[ ! -d {DIR_OUTPUTS} ]] && mkdir {DIR_OUTPUTS} ; exit 0"
    )

    @task
    def download_health_care_data():
        download.download_data(URL_HEALTH_CARE, CSV_HEALTH_CARE)

    @task
    def download_population_data():
        download.download_data(URL_POPULATION, CSV_POPOPULATION)
    
    @task
    def download_lau_nuts_map():
        download.download_data(URL_LAU_NUTS_MAP, CSV_LAU_NUTS_MAP)

    @task
    def create_population_datacube():
        population.create_population_datacube(CSV_POPOPULATION, CSV_LAU_NUTS_MAP, TTL_POPULATION)
    
    @task
    def create_health_care_datacube():
        health_care.create_health_care_datacube(CSV_HEALTH_CARE, TTL_HEALTH_CARE)

    create_data_dirs >> [download_lau_nuts_map(), download_population_data()] >> create_population_datacube()
    create_data_dirs >> download_health_care_data() >> create_health_care_datacube()
    

dag = create_datacubes()