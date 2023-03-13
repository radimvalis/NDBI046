#!/usr/bin/env python3

import csv, sys
from rdflib import Graph, URIRef, Literal, RDF, RDFS, XSD, QB 
from datacube import BASE_URI, RVO, create_health_care_QB, add_region_instance, add_county_instance, add_field_of_care_instance

def load_health_care_data(data_path):

    data = dict()

    with open(data_path, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        county_idx = header.index("OkresCode")
        region_idx = header.index("KrajCode")
        fields_of_care_idx = header.index("OborPece")

        for line in reader:

            region = line[region_idx]
            county = line[county_idx]
            fields_of_care = list(set([parts.strip() for parts in line[fields_of_care_idx].split(',')]))

            if not region:
                region = "UNKNOWN_REGION"

            if not region in data:
                data[region] = dict()
        
            if not county:
                county = "UNKNOWN_COUNTY"

            if not county in data[region]:
                data[region][county] = dict()

            for f in fields_of_care:

                if not f:
                    f = "OTHER_FIELDS"

                if f in data[region][county]:
                    data[region][county][f] += 1

                else:
                    data[region][county][f] = 1
    
    return data

def load_data_to_datacube(data, datacube: Graph, dataset_uri: URIRef):

    observed_fields_of_care = set()

    observation_id = 1

    for region, counties in data.items():

        region_instance = URIRef((f"{BASE_URI}/ontology#Regions/{region}"))
        add_region_instance(region_instance, region, datacube)

        for county, fields_of_care in counties.items():

            county_instance = URIRef((f"{BASE_URI}/ontology#Counties/{county}"))
            add_county_instance(county_instance, county, datacube)

            for f, count in fields_of_care.items():

                observation = URIRef(f"{BASE_URI}/observations/hc-{observation_id}")
                f_encoded = f.replace(" ", "-")

                field_of_care_instance = URIRef((f"{BASE_URI}/ontology#FieldsOfCare/{f_encoded}"))

                if field_of_care_instance not in observed_fields_of_care:
                    add_field_of_care_instance(field_of_care_instance, f, datacube)
                    
                datacube.add((observation, RDF.type, QB.Observation))
                datacube.add((observation, QB.dataSet, dataset_uri))
                datacube.add((observation, RVO.region, region_instance))
                datacube.add((observation, RVO.county, county_instance))
                datacube.add((observation, RVO.field_of_care, field_of_care_instance))
                datacube.add((observation, RVO.care_providers_count, Literal(count, datatype=XSD.integer)))

                observation_id += 1

    return datacube

def main():

    if len(sys.argv) == 1:
        print(f"{sys.argv[0]}: No data file provided", file=sys.stderr)
        return
    
    csv_data_path = sys.argv[1]
    dataset_uri = URIRef(f"{BASE_URI}/datasets/health_care")
    parsed_data = load_health_care_data(csv_data_path)
    datacube = create_health_care_QB(dataset_uri)
    datacube = load_data_to_datacube(parsed_data, datacube, dataset_uri)
    print(datacube.serialize(format="turtle"))

if __name__ == "__main__":
    main()