from create_smaller_query import *
from generateQuery import *
from lib import *
import csv

endpoint = "http://localhost:7200/repositories/one-million-repository"

testquery = "INSERT DATA { <http://db.uwaterloo.ca/~galuc/wsdbm/City101>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country2> . <http://db.uwaterloo.ca/~galuc/wsdbm/City102>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country17> . <http://db.uwaterloo.ca/~galuc/wsdbm/City103>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country3> . <http://db.uwaterloo.ca/~galuc/wsdbm/City104>    <http://www.geonames.org/ontology#parentCountry>    <http://db.uwaterloo.ca/~galuc/wsdbm/Country1> .}"


def main(name, amount):
    times = []
    data = [["time in msek", "amount of triples"]]
    input_querys = generate_query("database/two-million.nt", amount)
    for i in range(len(input_querys)):
        executing_query = QueryMaker(input_querys[i])
        print(i, "\n\n")
        times.append(GetTimeOfQuery(endpoint, executing_query))
        data.append([times[i]["time in ms"], 2**i])

    mode = "w"

    # Open the file in write mode with the CSV writer
    with open(name, mode, newline="") as file:
        writer = csv.writer(file)

        # Write each row of the 2D array as a separate row in the CSV file
        for row in data:
            writer.writerow(row)


# Move to lib.py later
def QueryMaker(query):
    dictionary = create_dict_based_on_query(query)
    new_query = create_void_select(dictionary)
    return new_query


main("data.csv", 15)
