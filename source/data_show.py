import csv

from generationData import *
from lib import *


def crate_new_file():

    files = ["database/eight-million.nt", "database/five-million.nt", "database/four-million.nt", "database/nine-million.nt", "database/seven-million.nt", "database/six-million.nt",  "database/ten-million.nt", "database/three-million.nt",  "database/one-million.nt"  ]
    with open('database/new_size_9mil', 'w') as outfile:
        for file_path in files:
            with open(file_path) as infile:
                outfile.write(infile.read())

def create_generation_data(
    endpoint,
    db_increase_file, name
):
    data_labels = [
        "generation time in msek",
        "dbsize in triples",
    ]
    dyn_labels = ["insert size", "insert time in msek", "dbsize in triples",]

    docker_reset_db()
    # Define the number of lines to send at a time
    chunk_size = 10000
    times_size_db = []
    dyn_times_db = []
    db_size = 1000000

    # Open the file for reading
    try:
        with open(db_increase_file, "r") as f:
            # Read the first chunk of lines
            lines = f.readlines(chunk_size)
            
            # Loop through the file and send chunks of lines to the endpoint
            while lines:
                # Join the lines into a string
                data = "".join(lines)
                query = "INSERT DATA {" + data + "}"
                create_datapoint(db_size, endpoint)
                dyn_times_db += create_dyn_datapoints(db_size, endpoint, lines)

                InsertDataQuery(endpoint, query)
                times_size_db.append(create_datapoint(db_size, endpoint))
                db_size += 10000
                print(db_size)
                if db_size > 10000000:
                    break
    except Exception as err:
        print(err)   
        
    with open(name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data_labels)
        # Write each row of the 2D array as a separate row in the CSV file
        for row in times_size_db:
            writer.writerow(row)
    with open("dyntime.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(dyn_labels)
        # Write each row of the 2D array as a separate row in the CSV file
        for row in dyn_times_db:
            writer.writerow(row)




def create_dyn_datapoints(db_size, endpoint, insert_data):
    data = []
    temp = []
    for i in range(1, 5001, 1000):
        ofsett = slice(0,i)
        insert_q = "INSERT DATA {" + "".join(insert_data[ofsett]) + "}"

        dynamic_query = QueryMaker(insert_q)
        dynamic_time = GetTimeOfQuery(endpoint,dynamic_query)["time in ms"]
        print(dynamic_time)
        temp.append(dynamic_time)
        temp.append(i)
        temp.append(db_size)
        data.append(temp)
    return data
    



def create_datapoint(db_size, endpoint):

    data = []
    generation_query = "SELECT (COUNT(*) AS ?totalTriples) (COUNT(DISTINCT ?subject) AS ?numSubjects) (COUNT(DISTINCT ?predicate) AS ?numPredicates) (COUNT(DISTINCT ?object) AS ?numObjects) WHERE { ?subject ?predicate ?object . }"
    generation_time = GetTimeOfQuery(endpoint, generation_query)["time in ms"]
    print("init gen",  generation_time)
    data.append(generation_time)
    data.append(db_size)
    
    return data

create_generation_data("http://localhost:7200/repositories/one-million-repository", 'database/new_size_9mil', "generation_data.csv" )