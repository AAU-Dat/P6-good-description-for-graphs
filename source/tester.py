from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from SPARQLWrapper import SPARQLWrapper, JSON

# set up the GraphDB endpoint
endpoint_url = "http://25e5f9df8e83:7200/repositories/Pokemans-rdf-DB"
sparql = SPARQLWrapper(endpoint_url)

# define the SPARQL query
query_string = """
PREFIX pokeball: <file:/uploaded/generated/pokeball.org/>

SELECT *
WHERE
{
?s ?p ?o.
}
"""

# set the query string and format
sparql.setQuery(query_string)
sparql.setReturnFormat(JSON)

# execute the query and parse the results
results = sparql.query().convert()

# iterate through the results and print them out
for result in results["results"]["bindings"]:
    print(result)
