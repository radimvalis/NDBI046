#!/usr/bin/env python3

from rdflib import Graph, Namespace, URIRef, Literal, RDF, DCAT, RDFS, XSD, DCTERMS

DISTR = Namespace("https://github.com/radimvalis/distributions/")
DATASET = Namespace("https://github.com/radimvalis/datasets/")

def create_dcat_dataset() -> Graph:

    graph = Graph()
    graph.bind("distr", DISTR)
    graph.bind("dataset", DATASET)

    DISTR_POPULATION = DISTR["population-2021"]

    graph.add((DISTR_POPULATION , RDF.type, DCAT.Distribution))
    graph.add((DISTR_POPULATION , DCTERMS.title, Literal("Population 2021", lang="en")))
    graph.add((DISTR_POPULATION , DCAT.accessURL, URIRef("https://github.com/radimvalis/NDBI046/blob/main/skos-dcat/datacube-population-2021.ttl")))
    graph.add((DISTR_POPULATION , DCAT.mediaType, URIRef("https://www.iana.org/assignments/media-types/text/turtle")))
    graph.add((DISTR_POPULATION , DCTERMS.format, URIRef("http://publications.europa.eu/resource/authority/file-type/RDF_TURTLE")))

    DATASET_POPULATION = DATASET["population-2021"]

    graph.add((DATASET_POPULATION, RDF.type, DCAT.Dataset))
    
    graph.add((DATASET_POPULATION, RDFS.label, Literal("Obyvatelstvo České republiky", lang="cs")))
    graph.add((DATASET_POPULATION, RDFS.label, Literal("Population of Czechia", lang="en")))
    graph.add((DATASET_POPULATION, DCTERMS.description, Literal("Datová sada popisující rozložení obyvatelstva v České republice", lang="cs")))
    graph.add((DATASET_POPULATION, DCTERMS.description, Literal("Dataset describing the distribution of population in Czechia", lang="en")))
    graph.add((DATASET_POPULATION, DCAT.distribution, DISTR_POPULATION))
    graph.add((DATASET_POPULATION, DCTERMS.accrualPeriodicity, URIRef("http://publications.europa.eu/resource/authority/frequency/NEVER")))
    graph.add((DATASET_POPULATION, DCTERMS.publisher, Literal("https://github.com/radimvalis/me", datatype=XSD.anyURI)))
    graph.add((DATASET_POPULATION, DCTERMS.spatial, URIRef("http://publications.europa.eu/resource/authority/country/CZE")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("obyvatelstvo", lang="cs")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("population", lang="en")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("rozložení obyvatelstva", lang="cs")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("distribution of population", lang="en")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("Česká republika", lang="cs")))
    graph.add((DATASET_POPULATION, DCAT.keyword, Literal("Czechia", lang="en")))
    graph.add((DATASET_POPULATION, DCAT.theme, URIRef("http://eurovoc.europa.eu/3300")))
    graph.add((DATASET_POPULATION, DCAT.theme, URIRef("http://eurovoc.europa.eu/5860")))
    graph.add((DATASET_POPULATION, DCAT.theme, URIRef("http://eurovoc.europa.eu/7816")))

    return graph

def main():
    dataset = create_dcat_dataset()
    print(dataset.serialize(format="turtle"))

if __name__ == "__main__":
    main()