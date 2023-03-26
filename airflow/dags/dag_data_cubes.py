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

CSV_HEALTH_CARE_PATH = DIR_INPUTS + "health-care.csv"
CSV_POPOPULATION_PATH = DIR_INPUTS + "population.csv"
CSV_LAU_NUTS_MAP_PATH = DIR_INPUTS +"lau-nuts-mapping.csv"

TTL_HEALTH_CARE = "health_care.ttl"
TTL_POPULATION = "population.ttl"

@dag(
    dag_id="data-cubes",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 26)
)

def create_datacubes():

    create_data_dirs = BashOperator(
        task_id="create_data_dirs",
        bash_command=f" [[ ! -d {DIR_INPUTS} ]] && mkdir {DIR_INPUTS} ; [[ ! -d {DIR_OUTPUTS} ]] && mkdir {DIR_OUTPUTS} ; exit 0"
    )

    @task(task_id="download_health_care_data")
    def download_health_care_data():
        download.download_data(URL_HEALTH_CARE, CSV_HEALTH_CARE_PATH)

    @task(task_id="download_population_data")
    def download_population_data():
        download.download_data(URL_POPULATION, CSV_POPOPULATION_PATH)
    
    @task(task_id="download_lau_nuts_map")
    def download_lau_nuts_map():
        download.download_data(URL_LAU_NUTS_MAP, CSV_LAU_NUTS_MAP_PATH)

    @task(task_id="create_health_care_datacube")
    def create_health_care_datacube(**kwargs):
        output_dir = kwargs["dag_run"].conf.get("output_path", TTL_HEALTH_CARE)
        health_care.create_health_care_datacube(CSV_HEALTH_CARE_PATH, output_dir + TTL_HEALTH_CARE)

    @task(task_id="create_population_datacube")
    def create_population_datacube(**kwargs):
        output_dir = kwargs["dag_run"].conf.get("output_path", TTL_POPULATION)
        population.create_population_datacube(CSV_POPOPULATION_PATH, CSV_LAU_NUTS_MAP_PATH, output_dir + TTL_POPULATION)
    
    create_data_dirs >> [download_lau_nuts_map(), download_population_data()] >> create_population_datacube()
    create_data_dirs >> download_health_care_data() >> create_health_care_datacube()
    

dag = create_datacubes()