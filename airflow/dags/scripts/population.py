#!/usr/bin/env python3

import csv, sys
from rdflib import Graph, URIRef, Literal, RDF, XSD, QB
from scripts.datacube import BASE_URI, RVO, create_population_QB, add_region_instance, add_county_instance, write

def load_NUTS_to_LAU_mapping(lau_nuts_map_path):

    NUTS_to_LAU_mapping = dict()

    with open(lau_nuts_map_path, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        LAU_code_idx = header.index("CHODNOTA1")
        NUTS_code_idx = header.index("CHODNOTA2")

        for line in reader:
            if line:
                NUTS_to_LAU_mapping[line[NUTS_code_idx]] = line[LAU_code_idx]
    
    return NUTS_to_LAU_mapping

def load_data_to_datacube(data_path, lau_nuts_map_path, datacube: Graph, dataset_uri: URIRef):
    
    mapping = load_NUTS_to_LAU_mapping(lau_nuts_map_path)

    with open(data_path, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        hodnota_idx = header.index("hodnota")
        vuk_idx = header.index("vuk")
        vuzemi_cis_idx = header.index("vuzemi_cis")
        vuzemi_kod_idx = header.index("vuzemi_kod")

        observed_regions = set()

        observation_id = 1

        for line in reader:

            # convert Prague(city) to Prague(county)

            if line[vuzemi_cis_idx] == "43" and line[vuzemi_kod_idx] == "554782":
                line[vuzemi_kod_idx] = "40924"
                line[vuzemi_cis_idx] = "101"

            if line[vuk_idx] == "DEM0004" and line[vuzemi_cis_idx] == "101":

                LAU_code = mapping[line[vuzemi_kod_idx]]
                region_code = LAU_code[:-1]

                region_instance = URIRef((f"{BASE_URI}/ontology#Regions/{region_code}"))

                if region_instance not in observed_regions:
                    add_region_instance(region_instance, region_code, datacube)

                county_instance = URIRef((f"{BASE_URI}/ontology#Counties/{LAU_code}"))
                add_county_instance(county_instance, LAU_code, datacube)

                observation = URIRef(f"https://github.com/radimvalis/observations/p-{observation_id}")

                datacube.add((observation, RDF.type, QB.Observation))
                datacube.add((observation, QB.dataSet, dataset_uri))
                datacube.add((observation, RVO.region, region_instance))
                datacube.add((observation, RVO.county, county_instance))
                datacube.add((observation, RVO.mean_population, Literal(line[hodnota_idx], datatype=XSD.integer)))

                observation_id += 1
    
    return datacube

def create_population_datacube(csv_data_path, lau_nuts_map_path, output_path = None):

    datacube = create_population_QB(URIRef(BASE_URI))
    dataset_uri = URIRef(f"{BASE_URI}/datasets/population-2021")
    datacube = load_data_to_datacube(csv_data_path, lau_nuts_map_path, datacube, dataset_uri)
    write(datacube, output_path)

def main():

    if len(sys.argv) < 3:
        print(f"{sys.argv[0]}: Missing CSV file(s)", file=sys.stderr)
        return
    
    if len(sys.argv == 3):
        create_population_datacube(csv_data_path = sys.argv[1], lau_nuts_map_path = sys.argv[2])

    else:
        create_population_datacube(csv_data_path = sys.argv[1], lau_nuts_map_path = sys.argv[2], output_path = sys.argv[3])

if __name__ == "__main__":
    main()