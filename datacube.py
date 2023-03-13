
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD, QB, DCTERMS, SKOS

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_DIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")

BASE_URI = "https://github.com/radimvalis"

class RVV:

    field_of_care = URIRef(f"{BASE_URI}/vocabulary/field_of_care")
    county = URIRef(f"{BASE_URI}/vocabulary/county")
    region = URIRef(f"{BASE_URI}/vocabulary/region")

class RVO:

    care_providers_count = URIRef(f"{BASE_URI}/ontology#care_providers_count")
    field_of_care = URIRef(f"{BASE_URI}/ontology#field_of_care")
    mean_population = URIRef(f"{BASE_URI}/ontology#mean_population")
    county = URIRef(f"{BASE_URI}/ontology#county")
    region = URIRef(f"{BASE_URI}/ontology#region")

def create_DSD(dsd_uri: URIRef, measure: URIRef, dimensions: list, datacube: Graph):

    datacube.add((dsd_uri, RDF.type, QB.DataStructureDefinition))

    # add measure

    component = BNode()
    datacube.add((component, QB.measure, measure))
    datacube.add((dsd_uri, QB.component, component))

    # add dimensions

    for dimension in dimensions:

        component = BNode()
        datacube.add((component, QB.dimension, dimension))
        datacube.add((dsd_uri, QB.component, component))

def add_region_instance(instance_uri, region_code, datacube: Graph):

    datacube.add((instance_uri, RDF.type, RVV.region))
    datacube.add((instance_uri, RDFS.label, Literal(region_code, lang="cs")))
    datacube.add((instance_uri, RDFS.label, Literal(region_code, lang="en")))

def add_county_instance(instance_uri, county_code, datacube: Graph):

    datacube.add((instance_uri, RDF.type, RVV.county))
    datacube.add((instance_uri, RDFS.label, Literal(county_code, lang="cs")))
    datacube.add((instance_uri, RDFS.label, Literal(county_code, lang="en")))

def add_field_of_care_instance(instance_uri, field_of_care, datacube: Graph):

    datacube.add((instance_uri, RDF.type, RVV.field_of_care))
    datacube.add((instance_uri, RDFS.label, Literal(field_of_care, lang="cs")))

def add_territorial_resources(datacube: Graph):

    datacube.add((RVV.region, RDF.type, RDFS.Class))
    datacube.add((RVV.region, RDFS.label, Literal("NUTS3-2004 code", lang="en")))
    datacube.add((RVV.region, RDFS.label, Literal("NUTS3-2004 kód", lang="cs")))
    datacube.add((RVV.region, SKOS.prefLabel, Literal("NUTS3-2004 code", lang="en")))
    datacube.add((RVV.region, SKOS.prefLabel, Literal("NUTS3-2004 kód", lang="cs")))

    datacube.add((RVV.county, RDF.type, RDFS.Class))
    datacube.add((RVV.county, RDFS.label, Literal("OKRES_LAU code", lang="en")))
    datacube.add((RVV.county, RDFS.label, Literal("OKRES_LAU kód", lang="cs")))
    datacube.add((RVV.county, SKOS.prefLabel, Literal("OKRES_LAU code", lang="en")))
    datacube.add((RVV.county, SKOS.prefLabel, Literal("OKRES_LAU kód", lang="cs")))

def add_field_of_care_resource(datacube: Graph):

    datacube.add((RVV.field_of_care, RDF.type, RDFS.Class))
    datacube.add((RVV.field_of_care, RDFS.label, Literal("field of care", lang="en")))
    datacube.add((RVV.field_of_care, RDFS.label, Literal("obor péče", lang="cs")))
    datacube.add((RVV.field_of_care, SKOS.prefLabel, Literal("field of care", lang="en")))
    datacube.add((RVV.field_of_care, SKOS.prefLabel, Literal("obor péče", lang="cs")))

def add_territorial_dimensions(datacube: Graph):

    datacube.add((RVO.region, RDF.type, RDF.Property))
    datacube.add((RVO.region, RDF.type, QB.DimensionProperty))
    datacube.add((RVO.region, RDFS.label, Literal("NUTS3-2004 code", lang="en")))
    datacube.add((RVO.region, RDFS.label, Literal("NUTS3-2004 kód", lang="cs")))
    datacube.add((RVO.region, RDFS.range, RVV.region))
    datacube.add((RVO.region, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    datacube.add((RVO.region, QB.concept, SDMX_CONCEPT.refArea))

    datacube.add((RVO.county, RDF.type, RDF.Property))
    datacube.add((RVO.county, RDF.type, QB.DimensionProperty))
    datacube.add((RVO.county, RDFS.label, Literal("OKRES_LAU code", lang="en")))
    datacube.add((RVO.county, RDFS.label, Literal("OKRES_LAU kód", lang="cs")))
    datacube.add((RVO.county, RDFS.range, RVV.county))
    datacube.add((RVO.county, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    datacube.add((RVO.county, QB.concept, SDMX_CONCEPT.refArea))

def add_field_of_care_dimension(datacube: Graph):

    datacube.add((RVO.field_of_care, RDF.type, RDF.Property))
    datacube.add((RVO.field_of_care, RDF.type, QB.DimensionProperty))
    datacube.add((RVO.field_of_care, RDFS.label, Literal("field of care", lang="en")))
    datacube.add((RVO.field_of_care, RDFS.label, Literal("obor péče", lang="cs")))
    datacube.add((RVO.field_of_care, RDFS.range, RVV.field_of_care))

def add_care_providers_count_measure(datacube: Graph):

    datacube.add((RVO.care_providers_count, RDF.type, RDF.Property))
    datacube.add((RVO.care_providers_count, RDF.type, QB.MeasureProperty))
    datacube.add((RVO.care_providers_count, RDFS.label, Literal("number of care providers", lang="en")))
    datacube.add((RVO.care_providers_count, RDFS.label, Literal("počet poskytovatelů zdravotní péče", lang="cs")))
    datacube.add((RVO.care_providers_count, RDFS.range, XSD.integer))
    datacube.add((RVO.care_providers_count, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))

def add_mean_population_measure(datacube: Graph):

    datacube.add((RVO.mean_population, RDF.type, RDF.Property))
    datacube.add((RVO.mean_population, RDF.type, QB.MeasureProperty))
    datacube.add((RVO.mean_population, RDFS.label, Literal("mean population", lang="en")))
    datacube.add((RVO.mean_population, RDFS.label, Literal("střední stav obyvatel", lang="cs")))
    datacube.add((RVO.mean_population, RDFS.range, XSD.integer))
    datacube.add((RVO.mean_population, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))

def add_health_care_metadata(dataset_uri, datacube: Graph):

    datacube.add((dataset_uri, DCTERMS.title, Literal("Care Providers", lang="en")))
    datacube.add((dataset_uri, DCTERMS.title, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    datacube.add((dataset_uri, RDFS.label, Literal("Care Providers", lang="en")))
    datacube.add((dataset_uri, RDFS.label, Literal("Poskytovatelé zdravotní péče", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datacube describing health care providers in the Czech Republic", lang="en")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující poskytovatele zdravotních služeb v České republice", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.publisher, Literal(f"{BASE_URI}/me", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.modified, Literal("2023-03-13",datatype=XSD.date)))
    datacube.add((dataset_uri, DCTERMS.issued, Literal("2023-03-13",datatype=XSD.date)))

def add_population_metadata(dataset_uri, datacube: Graph):

    datacube.add((dataset_uri, DCTERMS.title, Literal("Population In Counties 2021", lang="en")))
    datacube.add((dataset_uri, DCTERMS.title, Literal("Obyvatelé okresy 2021", lang="cs")))
    datacube.add((dataset_uri, RDFS.label, Literal("Population in districts 2021", lang="en")))
    datacube.add((dataset_uri, RDFS.label, Literal("Obyvatelé okresy 2021", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datacube describing population in the Czech Republic", lang="en")))
    datacube.add((dataset_uri, DCTERMS.description, Literal("Datová kostka popisující populaci České republiky", lang="cs")))
    datacube.add((dataset_uri, DCTERMS.publisher, Literal(f"{BASE_URI}/me", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.license, Literal("https://opensource.org/license/mit/", datatype=XSD.anyURI)))
    datacube.add((dataset_uri, DCTERMS.modified, Literal("2023-03-13",datatype=XSD.date)))
    datacube.add((dataset_uri, DCTERMS.issued, Literal("2023-03-13",datatype=XSD.date)))

def create_graph():

    graph = Graph()

    graph.bind("dct", DCTERMS)
    graph.bind("qb", QB)
    graph.bind("skos", SKOS)
    graph.bind("sdmx-concept", SDMX_CONCEPT)
    graph.bind("sdmx-dimension", SDMX_DIMENSION)
    graph.bind("sdmx-measure", SDMX_MEASURE)
    graph.bind("rvv", f"{BASE_URI}/vocabulary/")
    graph.bind("rvo", f"{BASE_URI}/ontology#")

    return graph

def create_health_care_QB(dataset_uri: URIRef):

    datacube = create_graph()

    add_territorial_resources(datacube)
    add_field_of_care_resource(datacube)

    add_territorial_dimensions(datacube)
    add_field_of_care_dimension(datacube)

    add_care_providers_count_measure(datacube)

    dsd_uri = URIRef(f"{BASE_URI}/dsd/health_care")
    measure = RVO.care_providers_count
    dimensions = [RVO.region, RVO.county, RVO.field_of_care]
    create_DSD(dsd_uri, measure, dimensions, datacube)

    # create dataset

    datacube.add((dataset_uri, RDF.type, QB.DataSet))
    datacube.add((dataset_uri, QB.structure, dsd_uri))

    add_health_care_metadata(dataset_uri, datacube)

    return datacube

def create_population_QB(dataset_uri: URIRef):

    datacube = create_graph()

    add_territorial_resources(datacube)

    add_territorial_dimensions(datacube)

    add_mean_population_measure(datacube)

    dsd_uri = URIRef(f"{BASE_URI}/dsd/population")
    measure = RVO.mean_population
    dimensions = [RVO.region, RVO.county]
    create_DSD(dsd_uri, measure, dimensions, datacube)

    # create dataset

    datacube.add((dataset_uri, RDF.type, QB.DataSet))
    datacube.add((dataset_uri, QB.structure, dsd_uri))

    add_population_metadata(dataset_uri, datacube)

    return datacube