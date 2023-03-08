
from rdflib import Graph, URIRef, BNode, Literal, RDF, RDFS, XSD, QB, DCTERMS
from os.path import getmtime
from datetime import datetime

BASE_URI = "https://github.com/radimvalis"

class RVV:

    care_providers_count = URIRef(f"{BASE_URI}/vocabulary/care_providers_count")
    field_of_care = URIRef(f"{BASE_URI}/vocabulary/fields_of_care")
    mean_population = URIRef(f"{BASE_URI}/vocabulary/mean_population")
    county = URIRef(f"{BASE_URI}/vocabulary/county")
    region = URIRef(f"{BASE_URI}/vocabulary/region")

def create_DSD(dsd_uri: URIRef, measure: URIRef, dimensions: list, graph: Graph):

    graph.add((dsd_uri, RDF.type, QB.DataStructureDefinition))

    # add measure

    bn = BNode()
    graph.add((bn, QB.measure, measure))
    graph.add((dsd_uri, QB.component, bn))

    # add dimensions

    for dimension in dimensions:

        bn = BNode()
        graph.add((bn, QB.dimension, dimension))
        graph.add((dsd_uri, QB.component, bn))
    
    return graph

def add_territorial_dimensions(graph: Graph):

    graph.add((RVV.region, RDF.type, RDF.Property))
    graph.add((RVV.region, RDF.type, QB.DimensionProperty))
    graph.add((RVV.region, RDFS.label, Literal("NUTS3-2004", lang="en")))
    graph.add((RVV.region, RDFS.label, Literal("NUTS3-2004", lang="cs")))
    graph.add((RVV.region, RDFS.range, XSD.string))

    graph.add((RVV.county, RDF.type, RDF.Property))
    graph.add((RVV.county, RDF.type, QB.DimensionProperty))
    graph.add((RVV.county, RDFS.label, Literal("OKRES_LAU", lang="en")))
    graph.add((RVV.county, RDFS.label, Literal("OKRES_LAU", lang="cs")))
    graph.add((RVV.county, RDFS.range, XSD.string))

    return graph

def create_graph():

    graph = Graph()

    graph.bind("dct", DCTERMS)
    graph.bind("qb", QB)
    graph.bind("rvv", f"{BASE_URI}/vocabulary/")

    return graph

def create_health_care_QB(dataset_uri: URIRef):

    graph = create_graph()

    # definiton of dimensions

    graph = add_territorial_dimensions(graph)

    graph.add((RVV.field_of_care, RDF.type, RDF.Property))
    graph.add((RVV.field_of_care, RDF.type, QB.DimensionProperty))
    graph.add((RVV.field_of_care, RDFS.label, Literal("field of care", lang="en")))
    graph.add((RVV.field_of_care, RDFS.label, Literal("obor péče", lang="cs")))
    graph.add((RVV.field_of_care, RDFS.range, XSD.string))

    # definition of measure

    graph.add((RVV.care_providers_count, RDF.type, RDF.Property))
    graph.add((RVV.care_providers_count, RDF.type, QB.MeasureProperty))
    graph.add((RVV.care_providers_count, RDFS.label, Literal("number of care providers", lang="en")))
    graph.add((RVV.care_providers_count, RDFS.label, Literal("počet poskytovatelů zdravotní péče", lang="cs")))
    graph.add((RVV.care_providers_count, RDFS.range, XSD.integer))

    # create data schema definition

    dsd_uri = URIRef(f"{BASE_URI}dsd/health_care")
    measure = RVV.care_providers_count
    dimensions = [RVV.region, RVV.county, RVV.field_of_care]

    graph = create_DSD(dsd_uri, measure, dimensions, graph)

    # create dataset

    graph.add((dataset_uri, RDF.type, QB.DataSet))
    graph.add((dataset_uri, QB.structure, dsd_uri))

    # add metadata

    graph.add((dataset_uri, DCTERMS.title, Literal("Care Providers", lang="en")))
    graph.add((dataset_uri, DCTERMS.title, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    graph.add((dataset_uri, RDFS.label, Literal("Care Providers", lang="en")))
    graph.add((dataset_uri, RDFS.label, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    graph.add((dataset_uri, DCTERMS.description, Literal("Datacube describing health care providers in the Czech Republic", lang="en")))
    graph.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující poskytovatele zdravotních služeb v České republice", lang="cs")))
    graph.add((dataset_uri, DCTERMS.publisher, Literal("https://github.com/radimvalis", datatype=XSD.anyURI)))
    graph.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    graph.add((dataset_uri, DCTERMS.modified, Literal(datetime.fromtimestamp(getmtime("datacube.py")),datatype=XSD.dateTime)))

    return graph

def create_population_QB(dataset_uri: URIRef):

    graph = create_graph()

    # definiton of dimensions

    graph = add_territorial_dimensions(graph)

    # definition of measure

    graph.add((RVV.mean_population, RDF.type, RDF.Property))
    graph.add((RVV.mean_population, RDF.type, QB.MeasureProperty))
    graph.add((RVV.mean_population, RDFS.label, Literal("mean population", lang="en")))
    graph.add((RVV.mean_population, RDFS.label, Literal("střední stav obyvatel", lang="cs")))
    graph.add((RVV.mean_population, RDFS.range, XSD.integer))

    # create data schema definition

    dsd_uri = URIRef(f"{BASE_URI}dsd/population")
    measure = RVV.mean_population
    dimensions = [RVV.region, RVV.county]

    graph = create_DSD(dsd_uri, measure, dimensions, graph)

    # create dataset

    graph.add((dataset_uri, RDF.type, QB.DataSet))
    graph.add((dataset_uri, QB.structure, dsd_uri))

    # add metadata

    graph.add((dataset_uri, DCTERMS.title, Literal("Population In Counties 2021", lang="en")))
    graph.add((dataset_uri, DCTERMS.title, Literal("Obyvatelé okresy 2021", lang="cs")))
    graph.add((dataset_uri, RDFS.label, Literal("Population in districts 2021", lang="en")))
    graph.add((dataset_uri, RDFS.label, Literal("Obyvatelé okresy 2021", lang="cs")))
    graph.add((dataset_uri, DCTERMS.description, Literal("Datacube describing population in the Czech Republic", lang="en")))
    graph.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující populaci České republiky", lang="cs")))
    graph.add((dataset_uri, DCTERMS.publisher, Literal("https://github.com/radimvalis", datatype=XSD.anyURI)))
    graph.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    graph.add((dataset_uri, DCTERMS.modified, Literal(datetime.fromtimestamp(getmtime("datacube.py")),datatype=XSD.dateTime)))

    return graph