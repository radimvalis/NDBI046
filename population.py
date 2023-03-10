#!/usr/bin/env python3

import csv, sys
from rdflib import Graph, URIRef, Literal, RDF, XSD, QB
from datacube import BASE_URI, RVV, create_population_QB

def load_NUTS_to_LAU_mapping():

    NUTS_to_LAU_mapping = dict()

    with open("lau-nuts-mapping.csv", "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        LAU_code_idx = header.index("CHODNOTA1")
        NUTS_code_idx = header.index("CHODNOTA2")

        for line in reader:
            if line:
                NUTS_to_LAU_mapping[line[NUTS_code_idx]] = line[LAU_code_idx]
    
    return NUTS_to_LAU_mapping

def load_data_to_datacube(data_path, datacube: Graph, dataset_uri: URIRef):
    
    mapping = load_NUTS_to_LAU_mapping()

    with open(data_path, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        hodnota_idx = header.index("hodnota")
        vuk_idx = header.index("vuk")
        vuzemi_cis_idx = header.index("vuzemi_cis")
        vuzemi_kod_idx = header.index("vuzemi_kod")

        observation_id = 1

        for line in reader:

            # convert Prague(city) to Prague(county)

            if line[vuzemi_cis_idx] == "43" and line[vuzemi_kod_idx] == "554782":
                line[vuzemi_kod_idx] = "40924"
                line[vuzemi_cis_idx] = "101"

            if line[vuk_idx] == "DEM0004" and line[vuzemi_cis_idx] == "101":

                LAU_code = mapping[line[vuzemi_kod_idx]]

                observation = URIRef(f"https://github.com/radimvalis/observations/p-{observation_id}")

                datacube.add((observation, RDF.type, QB.Observation))
                datacube.add((observation, QB.dataSet, dataset_uri))
                datacube.add((observation, RVV.region, Literal(LAU_code[:-1], lang="cs")))
                datacube.add((observation, RVV.county, Literal(LAU_code, lang="cs")))
                datacube.add((observation, RVV.mean_population, Literal(line[hodnota_idx], datatype=XSD.integer)))

                observation_id += 1
    
    return datacube


def main():

    if len(sys.argv) == 1:
        print(f"{sys.argv[0]}: No data file provided", file=sys.stderr)
        return

    data_path = sys.argv[1]
    datacube = create_population_QB(URIRef(BASE_URI))
    dataset_uri = URIRef(f"{BASE_URI}/datasets/population-2021")
    datacube = load_data_to_datacube(data_path, datacube, dataset_uri)
    print(datacube.serialize(format="turtle"))

if __name__ == "__main__":
    main()