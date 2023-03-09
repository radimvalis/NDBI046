#!/usr/bin/env python3

import csv, sys
from rdflib import Graph, URIRef, Literal, RDF, XSD, QB 
from datacube import BASE_URI, RVV, create_health_care_QB

def load_health_care_data(data_path):

    data = dict()

    with open(data_path, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        district_idx = header.index("OkresCode")
        region_idx = header.index("KrajCode")
        fields_of_care_idx = header.index("OborPece")

        for line in reader:

            region = line[region_idx]
            district = line[district_idx]
            fields_of_care = list(set([parts.strip() for parts in line[fields_of_care_idx].split(',')]))

            if not region:
                region = "ostatní kraje"

            if not region in data:
                data[region] = dict()
            
            if not district in data[region]:
                data[region][district] = dict()

            for f in fields_of_care:

                if not f:
                    f = "ostatní obory péče"

                if f in data[region][district]:
                    data[region][district][f] += 1

                else:
                    data[region][district][f] = 1
    
    return data

def load_data_to_graph(data, graph: Graph, dataset_uri: URIRef):

    observation_id = 1

    for region, districts in data.items():
        for district, fields_of_care in districts.items():
            for f, count in fields_of_care.items():

                observation = URIRef(f"{BASE_URI}/observations/hc-{observation_id}")

                graph.add((observation, RDF.type, QB.Observation))
                graph.add((observation, QB.dataSet, dataset_uri))
                graph.add((observation, RVV.region, Literal(region, lang="cs")))
                graph.add((observation, RVV.county, Literal(district, lang="cs")))
                graph.add((observation, RVV.field_of_care, Literal(f, lang="cs")))
                graph.add((observation, RVV.care_providers_count, Literal(count, datatype=XSD.integer)))

                observation_id += 1

    return graph
    

def main():

    if len(sys.argv) == 1:
        print(f"{sys.argv[0]}: No data file provided", file=sys.stderr)
        return
    
    data_path = sys.argv[1]
    dataset_uri = URIRef(f"{BASE_URI}/datasets/health_care")
    parsed_data = load_health_care_data(data_path)
    graph = create_health_care_QB(dataset_uri)
    graph = load_data_to_graph(parsed_data, graph, dataset_uri)
    print(graph.serialize(format="turtle"))

if __name__ == "__main__":
    main()