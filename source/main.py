import json
from getData import PokemonQuery, InsertQuery
from voidCreator import VoidCreator

# Define the endpoint and query
endpoint = "http://localhost:7200/repositories/Pokemans-rdf-DB"
# getAllDataQuery = """ PREFIX pokeball: <file:/uploaded/generated/pokeball.org/>

# SELECT *
# WHERE
# {
# ?s ?p ?o.

# }
# LIMIT 5 """

testVoid = """
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
INSERT DATA{
    <http://example.com> a void:Dataset ;
        rdfs:label "Example" ;
        void:description "This is an example" ;
        void:uriSpace "http://example.com" ;
        void:entities 6 ;
        void:properties 1 ;
        void:distinctSubjects 3 ;
        void:distinctObjects 2 .
    }"""

InsertQuery(endpoint, testVoid)

# allDataJson = PokemonQuery(endpoint, getAllDataQuery)
# # allData = json.loads(allDataJson)

# voidDescription = VoidCreator(allDataJson)
# # print(voidDescription)
