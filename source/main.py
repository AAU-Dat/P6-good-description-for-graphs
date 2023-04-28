from create_smaller_query import *
from generateQuery import *
from lib import *

<<<<<<< HEAD
endpoint = "http://localhost:7200/repositories/one-million-repository"
=======
# The endpoint of the repository
# endpoint = "http://localhost:7200/repositories/Pokemans-rdf-DB"
endpoint = "http://localhost:7200/repositories/pokemon-repository"
>>>>>>> 90c93c8c7110933271594982e411fed8396f4e6e

testquery = "INSERT DATA { <http://db.uwaterloo.ca/~galuc/wsdbm/City101>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country2> . <http://db.uwaterloo.ca/~galuc/wsdbm/City102>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country17> . <http://db.uwaterloo.ca/~galuc/wsdbm/City103>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country3> . <http://db.uwaterloo.ca/~galuc/wsdbm/City104>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country1> .}"

<<<<<<< HEAD
def main():
    times = []
    input_querys = generate_query("database/two-million.nt", 10)
    for  i in range(len(input_querys)):
        executing_query = QueryMaker(input_querys[i])
        print(i, "\n\n")
        times.append(GetTimeOfQuery(endpoint, executing_query))

#Move to lib.py later
def QueryMaker(query):
    dictionary = create_dict_based_on_query(query)
    new_query = create_void_select(dictionary)
    return new_query

# main()
# result = generate_query("database/two-million.nt", 8)
# result = QueryMaker(result[7])
# result = GetTimeOfQuery(endpoint, result)
# print(result)
print(GetTimeOfQuery(endpoint, "SELECT (COUNT(*) AS ?totalTriples) (COUNT(DISTINCT ?subject) AS ?numSubjects) (COUNT(DISTINCT ?predicate) AS ?numPredicates) (COUNT(DISTINCT ?object) AS ?numObjects) WHERE { ?subject ?predicate ?object . }"))
=======
# Create a void description, using a given title, a short description and the data from the query
voidInsertQuery = VoidCreator("PokemonDB", "A base void description", dataSet)
print(voidInsertQuery)
# Insert the void description into the repository
# InsertDataQuery(endpoint, voidInsertQuery)
>>>>>>> 90c93c8c7110933271594982e411fed8396f4e6e
