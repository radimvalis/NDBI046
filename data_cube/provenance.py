from rdflib import Graph, BNode, URIRef, Literal, PROV, RDF, RDFS
from datacube import BASE_URI

class Entity:

    datacube_base_uri = BASE_URI + "/datasets/"
    csv_base_uri = BASE_URI + "/csv/"
    sparql_base_uri = BASE_URI + "/sparql/"

    datacube_health_care = URIRef(datacube_base_uri + "health_care")
    datacube_population = URIRef(datacube_base_uri + "population-2021")

    csv_health_care = URIRef(csv_base_uri + "health-care")
    csv_population = URIRef(csv_base_uri + "population")
    csv_lau_nuts_map = URIRef(csv_base_uri + "lau-nuts-map")

    sparql_queries = URIRef(sparql_base_uri + "validation-queries")

class Agent:

    software_agent_base_uri = BASE_URI + "/agents/"

    author = URIRef(BASE_URI + "/me")

    download = URIRef(software_agent_base_uri + "download")
    datacube = URIRef(software_agent_base_uri + "datacube")
    population = URIRef(software_agent_base_uri + "population")
    health_care = URIRef(software_agent_base_uri + "health_care")
    validation = URIRef(software_agent_base_uri + "validation")

class Activity:

    activity_base_uri = BASE_URI + "/activities/"

    download_data = URIRef(activity_base_uri + "download-data")
    create_population = URIRef(activity_base_uri + "create-population-datacube")
    create_health_care = URIRef(activity_base_uri + "create-health-care-datacube")
    validate_datacubes = URIRef(activity_base_uri + "validate-datacubes")

class Role:

    role_base_uri = BASE_URI + "/roles/"

    data_downloader = URIRef((role_base_uri + "data-downloader"))
    dsd_creator = URIRef((role_base_uri + "data-schema-definition-creator"))
    data_processor = URIRef((role_base_uri + "data-processor"))
    datacube_validator = URIRef((role_base_uri + "datacube-validator"))


def add_agents(provenance: Graph):

    provenance.add((Agent.author, RDF.type, PROV.Agent))
    provenance.add((Agent.author, RDF.type, PROV.Person))

    provenance.add((Agent.download, RDF.type, PROV.Agent))
    provenance.add((Agent.download, RDF.type, PROV.SoftwareAgent))
    provenance.add((Agent.download, PROV.actedOnBehalfOf, Agent.author))

    provenance.add((Agent.datacube, RDF.type, PROV.Agent))
    provenance.add((Agent.datacube, RDF.type, PROV.SoftwareAgent))
    provenance.add((Agent.datacube, PROV.actedOnBehalfOf, Agent.author))

    provenance.add((Agent.population, RDF.type, PROV.Agent))
    provenance.add((Agent.population, RDF.type, PROV.SoftwareAgent))
    provenance.add((Agent.population, PROV.actedOnBehalfOf, Agent.author))

    provenance.add((Agent.health_care, RDF.type, PROV.Agent))
    provenance.add((Agent.health_care, RDF.type, PROV.SoftwareAgent))
    provenance.add((Agent.health_care, PROV.actedOnBehalfOf, Agent.author))

    provenance.add((Agent.validation, RDF.type, PROV.Agent))
    provenance.add((Agent.validation, RDF.type, PROV.SoftwareAgent))
    provenance.add((Agent.validation, PROV.actedOnBehalfOf, Agent.author))

def add_entities(provencance: Graph):

    provencance.add((Entity.csv_lau_nuts_map, RDF.type, PROV.Entity))
    provencance.add((Entity.csv_lau_nuts_map, PROV.wasGeneratedBy, Activity.download_data))
    
    provencance.add((Entity.csv_health_care, RDF.type, PROV.Entity))
    provencance.add((Entity.csv_health_care, PROV.wasGeneratedBy, Activity.download_data))

    provencance.add((Entity.csv_population, RDF.type, PROV.Entity))
    provencance.add((Entity.csv_population, PROV.wasGeneratedBy, Activity.download_data))

    provencance.add((Entity.datacube_health_care, RDF.type, PROV.Entity))
    provencance.add((Entity.datacube_health_care, PROV.wasGeneratedBy, Activity.create_health_care))
    provencance.add((Entity.datacube_health_care, PROV.wasDerivedFrom, Entity.csv_health_care))

    provencance.add((Entity.datacube_population, RDF.type, PROV.Entity))
    provencance.add((Entity.datacube_population, PROV.wasGeneratedBy, Activity.create_population))
    provencance.add((Entity.datacube_population, PROV.wasDerivedFrom, Entity.csv_lau_nuts_map))
    provencance.add((Entity.datacube_population, PROV.wasDerivedFrom, Entity.csv_population))

    provencance.add((Entity.sparql_queries, RDF.type, PROV.Entity))

def add_roles(provenance: Graph):

    provenance.add((Role.data_downloader, RDF.type, PROV.Role))
    provenance.add((Role.dsd_creator, RDF.type, PROV.Role))
    provenance.add((Role.data_processor, RDF.type, PROV.Role))
    provenance.add((Role.datacube_validator, RDF.type, PROV.Role))

def add_download_actitity(provenance: Graph):

    provenance.add((Activity.download_data, RDF.type, PROV.Activity))

    provenance.add((Activity.download_data, PROV.generated, Entity.csv_lau_nuts_map))
    provenance.add((Activity.download_data, PROV.generated, Entity.csv_health_care))
    provenance.add((Activity.download_data, PROV.generated, Entity.csv_population))

    association = BNode()
    provenance.add((Activity.download_data, PROV.qualifiedAssociation, association))
    provenance.add((association, RDF.type, PROV.Association))
    provenance.add((association, PROV.agent, Agent.download))
    provenance.add((association, PROV.hadRole, Role.data_downloader))
    provenance.add((association, RDFS.comment, Literal("Downloaded all required data from the web.", lang="en")))

def add_health_care_activity(provenance: Graph):

    provenance.add((Activity.create_health_care, RDF.type, PROV.Activity))
    provenance.add((Activity.create_health_care, PROV.used, Entity.csv_health_care))
    provenance.add((Activity.create_health_care, PROV.generated, Entity.datacube_health_care))

    dsd_creator_association = BNode()
    provenance.add((Activity.create_health_care, PROV.qualifiedAssociation, dsd_creator_association))
    provenance.add((dsd_creator_association, RDF.type, PROV.Association))
    provenance.add((dsd_creator_association, PROV.agent, Agent.datacube))
    provenance.add((dsd_creator_association, PROV.hadRole, Role.dsd_creator))
    provenance.add((dsd_creator_association, RDFS.comment, Literal("Created data schema definition for health care datacube", lang="en")))

    data_processor_association = BNode()
    provenance.add((Activity.create_health_care, PROV.qualifiedAssociation, data_processor_association))
    provenance.add((data_processor_association, RDF.type, PROV.Association))
    provenance.add((data_processor_association, PROV.agent, Agent.health_care))
    provenance.add((data_processor_association, PROV.hadRole, Role.data_processor))
    provenance.add((data_processor_association, RDFS.comment, Literal("Transformed CSV into observations", lang="en")))

def add_population_activity(provenance: Graph):

    provenance.add((Activity.create_population, RDF.type, PROV.Activity))
    provenance.add((Activity.create_population, PROV.used, Entity.csv_population))
    provenance.add((Activity.create_population, PROV.used, Entity.csv_lau_nuts_map))
    provenance.add((Activity.create_population, PROV.generated, Entity.datacube_population))

    dsd_creator_association = BNode()
    provenance.add((Activity.create_population, PROV.qualifiedAssociation, dsd_creator_association))
    provenance.add((dsd_creator_association, RDF.type, PROV.Association))
    provenance.add((dsd_creator_association, PROV.agent, Agent.datacube))
    provenance.add((dsd_creator_association, PROV.hadRole, Role.dsd_creator))
    provenance.add((dsd_creator_association, RDFS.comment, Literal("Created data schema definition for population datacube", lang="en")))

    data_processor_association = BNode()
    provenance.add((Activity.create_population, PROV.qualifiedAssociation, data_processor_association))
    provenance.add((data_processor_association, RDF.type, PROV.Association))
    provenance.add((data_processor_association, PROV.agent, Agent.population))
    provenance.add((data_processor_association, PROV.hadRole, Role.data_processor))
    provenance.add((data_processor_association, RDFS.comment, Literal("Transformed CSV into observations", lang="en")))

def add_validate_activity(provenance: Graph):

    provenance.add((Activity.validate_datacubes, RDF.type, PROV.Activity))
    provenance.add((Activity.validate_datacubes, PROV.used, Entity.datacube_health_care))
    provenance.add((Activity.validate_datacubes, PROV.used, Entity.datacube_population))

    validator_association = BNode()
    provenance.add((Activity.validate_datacubes, PROV.qualifiedAssociation, validator_association))
    provenance.add((validator_association, RDF.type, PROV.Association))
    provenance.add((validator_association, PROV.agent, Agent.validation))
    provenance.add((validator_association, PROV.hadRole, Role.datacube_validator))
    provenance.add((validator_association, RDFS.comment, Literal("Validated created data cubes", lang="en")))

def add_activities(provenance: Graph):

    add_download_actitity(provenance)
    add_health_care_activity(provenance)
    add_population_activity(provenance)
    add_validate_activity(provenance)

def create_graph():

    graph = Graph()

    graph.bind("prov", PROV)
    graph.bind("rv-datacube-entity", Entity.datacube_base_uri)
    graph.bind("rv-csv-entity", Entity.csv_base_uri)
    graph.bind("rv-sparql-entity", Entity.sparql_base_uri)
    graph.bind("rv-agent", Agent.software_agent_base_uri)
    graph.bind("rv-activity", Activity.activity_base_uri)
    graph.bind("rv-role", Role.role_base_uri)

    return graph


def generate_provenance():

    provenance = create_graph()

    add_agents(provenance)
    add_entities(provenance)
    add_activities(provenance)

    print(provenance.serialize(format="trig"))

def main():
    generate_provenance()

if __name__ == "__main__":
    main()