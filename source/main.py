from lib import *

# The endpoint of the repository
# endpoint = "http://localhost:7200/repositories/Pokemans-rdf-DB"
endpoint = "http://localhost:7200/repositories/pokemon-repository"

# a SPARQL query to get all the triples in the repository
query = """
    SELECT * WHERE {
        ?s ?p ?o .
    }
"""
# Queries the data from the query and stores it in a variable with SelectQuery()
dataSet = SelectQuery(endpoint, query)

# Create a void description, using a given title, a short description and the data from the query
voidInsertQuery = VoidCreator("PokemonDB", "A base void description", dataSet)
print(voidInsertQuery)
# Insert the void description into the repository
# InsertDataQuery(endpoint, voidInsertQuery)
