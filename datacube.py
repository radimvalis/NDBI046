
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD, QB, DCTERMS
from os.path import getmtime
from datetime import datetime

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_DIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")

BASE_URI = "https://github.com/radimvalis"

class RVV:

    care_providers_count = URIRef(f"{BASE_URI}/vocabulary/care_providers_count")
    field_of_care = URIRef(f"{BASE_URI}/vocabulary/fields_of_care")
    mean_population = URIRef(f"{BASE_URI}/vocabulary/mean_population")
    county = URIRef(f"{BASE_URI}/vocabulary/county")
    region = URIRef(f"{BASE_URI}/vocabulary/region")

def create_DSD(dsd_uri: URIRef, measure: URIRef, dimensions: list, datacube: Graph):

    datacube.add((dsd_uri, RDF.type, QB.DataStructureDefinition))

    # add measure

    bn = BNode()
    datacube.add((bn, QB.measure, measure))
    datacube.add((dsd_uri, QB.component, bn))

    # add dimensions

    for dimension in dimensions:

        bn = BNode()
        datacube.add((bn, QB.dimension, dimension))
        datacube.add((dsd_uri, QB.component, bn))
    
    return datacube

def add_territorial_dimensions(datacube: Graph):

    datacube.add((RVV.region, RDF.type, RDF.Property))
    datacube.add((RVV.region, RDF.type, QB.DimensionProperty))
    datacube.add((RVV.region, RDFS.label, Literal("NUTS3-2004 code", lang="en")))
    datacube.add((RVV.region, RDFS.label, Literal("NUTS3-2004 kód", lang="cs")))
    datacube.add((RVV.region, RDFS.range, XSD.string))
    datacube.add((RVV.region, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    datacube.add((RVV.region, QB.concept, SDMX_CONCEPT.refArea))

    datacube.add((RVV.county, RDF.type, RDF.Property))
    datacube.add((RVV.county, RDF.type, QB.DimensionProperty))
    datacube.add((RVV.county, RDFS.label, Literal("OKRES_LAU code", lang="en")))
    datacube.add((RVV.county, RDFS.label, Literal("OKRES_LAU kód", lang="cs")))
    datacube.add((RVV.county, RDFS.range, XSD.string))
    datacube.add((RVV.county, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    datacube.add((RVV.county, QB.concept, SDMX_CONCEPT.refArea))

    return datacube

def create_graph():

    datacube = Graph()

    datacube.bind("dct", DCTERMS)
    datacube.bind("qb", QB)
    datacube.bind("sdmx-concept", SDMX_CONCEPT)
    datacube.bind("sdmx-dimension", SDMX_DIMENSION)
    datacube.bind("sdmx-measure", SDMX_MEASURE)
    datacube.bind("rvv", f"{BASE_URI}/vocabulary/")

    return datacube

def create_health_care_QB(dataset_uri: URIRef):

    datacube = create_graph()

    # definiton of dimensions

    datacube = add_territorial_dimensions(datacube)

    datacube.add((RVV.field_of_care, RDF.type, RDF.Property))
    datacube.add((RVV.field_of_care, RDF.type, QB.DimensionProperty))
    datacube.add((RVV.field_of_care, RDFS.label, Literal("field of care", lang="en")))
    datacube.add((RVV.field_of_care, RDFS.label, Literal("obor péče", lang="cs")))
    datacube.add((RVV.field_of_care, RDFS.range, XSD.string))

    # definition of measure

    datacube.add((RVV.care_providers_count, RDF.type, RDF.Property))
    datacube.add((RVV.care_providers_count, RDF.type, QB.MeasureProperty))
    datacube.add((RVV.care_providers_count, RDFS.label, Literal("number of care providers", lang="en")))
    datacube.add((RVV.care_providers_count, RDFS.label, Literal("počet poskytovatelů zdravotní péče", lang="cs")))
    datacube.add((RVV.care_providers_count, RDFS.range, XSD.integer))
    datacube.add((RVV.care_providers_count, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))

    # create data schema definition

    dsd_uri = URIRef(f"{BASE_URI}/dsd/health_care")
    measure = RVV.care_providers_count
    dimensions = [RVV.region, RVV.county, RVV.field_of_care]

    datacube = create_DSD(dsd_uri, measure, dimensions, datacube)

    # create dataset

    datacube.add((dataset_uri, RDF.type, QB.DataSet))
    datacube.add((dataset_uri, QB.structure, dsd_uri))

    # add metadata

    datacube.add((dataset_uri, DCTERMS.title, Literal("Care Providers", lang="en")))
    datacube.add((dataset_uri, DCTERMS.title, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    datacube.add((dataset_uri, RDFS.label, Literal("Care Providers", lang="en")))
    datacube.add((dataset_uri, RDFS.label, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datacube describing health care providers in the Czech Republic", lang="en")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující poskytovatele zdravotních služeb v České republice", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.publisher, Literal(f"{BASE_URI}/me", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.modified, Literal(datetime.fromtimestamp(getmtime("datacube.py")),datatype=XSD.dateTime)))

    return datacube

def create_population_QB(dataset_uri: URIRef):

    datacube = create_graph()

    # definiton of dimensions

    datacube = add_territorial_dimensions(datacube)

    # definition of measure

    datacube.add((RVV.mean_population, RDF.type, RDF.Property))
    datacube.add((RVV.mean_population, RDF.type, QB.MeasureProperty))
    datacube.add((RVV.mean_population, RDFS.label, Literal("mean population", lang="en")))
    datacube.add((RVV.mean_population, RDFS.label, Literal("střední stav obyvatel", lang="cs")))
    datacube.add((RVV.mean_population, RDFS.range, XSD.integer))
    datacube.add((RVV.mean_population, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))

    # create data schema definition

    dsd_uri = URIRef(f"{BASE_URI}/dsd/population")
    measure = RVV.mean_population
    dimensions = [RVV.region, RVV.county]

    datacube = create_DSD(dsd_uri, measure, dimensions, datacube)

    # create dataset

    datacube.add((dataset_uri, RDF.type, QB.DataSet))
    datacube.add((dataset_uri, QB.structure, dsd_uri))

    # add metadata

    datacube.add((dataset_uri, DCTERMS.title, Literal("Population In Counties 2021", lang="en")))
    datacube.add((dataset_uri, DCTERMS.title, Literal("Obyvatelé okresy 2021", lang="cs")))
    datacube.add((dataset_uri, RDFS.label, Literal("Population in districts 2021", lang="en")))
    datacube.add((dataset_uri, RDFS.label, Literal("Obyvatelé okresy 2021", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datacube describing population in the Czech Republic", lang="en")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující populaci České republiky", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.publisher, Literal(f"{BASE_URI}/me", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.modified, Literal(datetime.fromtimestamp(getmtime("datacube.py")),datatype=XSD.dateTime)))

    return datacube