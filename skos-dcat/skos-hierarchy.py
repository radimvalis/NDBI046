#!/usr/bin/env python3

import os
import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, SKOS, DCTERMS, XSD
import requests

BASE_URI = "https://github.com/radimvalis"

POPULATION_CSV = "population-2021.csv"
LAU_NUTS_MAP_CSV = "lau-nuts-map.csv"

RVCS = Namespace(BASE_URI + "/concept-schemes")

def download_data(data_url: str, output_path: str):

    if not os.path.isfile(output_path):
        response = requests.get(data_url, stream=True, verify=False)
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=4096):
                file.write(chunk)

def create_collector() -> Graph:

    colllector = Graph()
    colllector.bind("rvcs", RVCS)
    return colllector

def load_nuts_lau_map():

    nuts_lau_map = dict()

    with open(LAU_NUTS_MAP_CSV, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        LAU_code_idx = header.index("CHODNOTA1")
        NUTS_code_idx = header.index("CHODNOTA2")

        for line in reader:
            if line:
                nuts_lau_map[line[NUTS_code_idx]] = line[LAU_code_idx]
    
    return nuts_lau_map

def add_concept_scheme(collector: Graph):

    collector.add((RVCS.territorial_units, RDF.type, SKOS.ConceptScheme))
    collector.add((RVCS.territorial_units, DCTERMS.title, Literal("Územní jednotky České republiky", lang="cs")))
    collector.add((RVCS.territorial_units, DCTERMS.title, Literal("Territorial units of Czechia", lang="en")))
    collector.add((RVCS.territorial_units, DCTERMS.creator, Literal("https://github.com/radimvalis/me", datatype=XSD.anyURI)))

def add_concept(concept_uri, pref_label, collector: Graph):

    collector.add((concept_uri, RDF.type, SKOS.Concept))
    collector.add((concept_uri, SKOS.prefLabel, Literal(pref_label, lang="cs")))
    collector.add((concept_uri, SKOS.inScheme, RVCS.territorial_units))

def add_top_concept(concept_uri, pref_label, collector: Graph):

    add_concept(concept_uri, pref_label, collector)
    collector.add((concept_uri, SKOS.topConceptOf, RVCS.territorial_units))
    collector.add((RVCS.territorial_units, SKOS.hasTopConcept, concept_uri))

def add_concept_relation(concept_narrower, concept_broader, collector: Graph):

    collector.add((concept_broader, SKOS.inScheme, RVCS.territorial_units))
    collector.add((concept_narrower, SKOS.inScheme, RVCS.territorial_units))

    collector.add((concept_narrower, SKOS.broader, concept_broader))
    collector.add((concept_broader, SKOS.narrower, concept_narrower))

def create_skos_hierarchy():

    nuts_lau_map = load_nuts_lau_map()
    collector = create_collector()

    add_concept_scheme(collector)

    regions_map = {
        "CZ020": "Středočeský kraj",
        "CZ031": "Jihočeský kraj",
        "CZ032": "Plzeňský kraj",
        "CZ041": "Karlovarský kraj",
        "CZ042": "Ústecký kraj",
        "CZ051": "Liberecký kraj",
        "CZ052": "Královéhradecký kraj",
        "CZ053": "Pardubický kraj",
        "CZ063": "Kraj Vysočina",
        "CZ064": "Jihomoravský kraj",
        "CZ071": "Olomoucký kraj",
        "CZ072": "Zlínský kraj",
        "CZ080": "Moravskoslezský kraj"
    }

    for region_code, region in regions_map.items():

        region_instance = URIRef(BASE_URI + "/ontology#Regions/" + region_code)
        add_top_concept(region_instance, region, collector)

    with open(POPULATION_CSV, "r") as stream:

        reader = csv.reader(stream)

        header = next(reader)

        vuk_idx = header.index("vuk")
        vuzemi_cis_idx = header.index("vuzemi_cis")
        vuzemi_kod_idx = header.index("vuzemi_kod")
        vuzemi_txt_idx = header.index("vuzemi_txt")

        for line in reader:

            # convert Prague - city to Prague - county
            if line[vuzemi_cis_idx] == "43" and line[vuzemi_kod_idx] == "554782":

                line[vuzemi_kod_idx] = "40924"
                line[vuzemi_cis_idx] = "101"

            if line[vuk_idx] == "DEM0004" and line[vuzemi_cis_idx] == "101":

                county_code = nuts_lau_map[line[vuzemi_kod_idx]]
                county_name = line[vuzemi_txt_idx]
                region_code = county_code[:-1]

                region_instance = URIRef(BASE_URI + "/ontology#Regions/" + region_code)
                county_instance = URIRef(BASE_URI + "/ontology#Counties/" + county_code)

                add_concept(county_instance, county_name, collector)
                add_concept_relation(county_instance, region_instance, collector)
    
    return collector

def main():
    
    download_data(
        "https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv",
        POPULATION_CSV
    )
    download_data(
        "https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/%C4%8D%C3%ADseln%C3%ADk-okres%C5%AF-vazba-101-nad%C5%99%C3%ADzen%C3%BD.csv",
        LAU_NUTS_MAP_CSV
    )

    hierarchy = create_skos_hierarchy()
    print(hierarchy.serialize(format="turtle"))


if __name__ == "__main__":
    main()