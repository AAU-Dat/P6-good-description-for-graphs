from lib import *
import os
import math


def datageneration(
    database_increment_func,
    maximum_db_size_added,
    querysize_increment_func,
    maximum_querysize,
    endpoint,
    db_increase_file,
    querysize_increase_file,
):
    data = []
    # right now maximum of maximums is 1 mil since our datasets are at most one mil
    db_size = 1000000

    res = []
    i = 0
    j = 1
    while i < maximum_db_size_added:
        j = 1
        while j < maximum_querysize:
            docker_reset_db()
            initial_insert = generate_insert_array(i, db_increase_file, 10000)
            for z in range(len(initial_insert)):
                InsertDataQuery(endpoint, initial_insert[z])
            
            data.append(create_data(j, db_size + i, querysize_increase_file, endpoint))
            j = querysize_increment_func(j)
        i = database_increment_func(i)
    return data







def create_data(size_of_insert, db_size_before_insert, file_to_generate_from, endpoint):
    data = []

    generation_query = "SELECT (COUNT(*) AS ?totalTriples) (COUNT(DISTINCT ?subject) AS ?numSubjects) (COUNT(DISTINCT ?predicate) AS ?numPredicates) (COUNT(DISTINCT ?object) AS ?numObjects) WHERE { ?subject ?predicate ?object . }"
    generation_time = GetTimeOfQuery(endpoint, generation_query)["time in ms"]
    print("init gen",  generation_time)
    insert_q = generate_insert(size_of_insert, file_to_generate_from)
    dynamic_query = QueryMaker(insert_q)
    dynamic_time = GetTimeOfQuery(endpoint,dynamic_query)["time in ms"]
    print("got dynamic time:", dynamic_time, "size of insert:", size_of_insert)
    InsertDataQuery(endpoint, insert_q)
    generation_time = GetTimeOfQuery(endpoint, generation_query)["time in ms"]
    print("got generation time:", generation_time, "db size:", db_size_before_insert)
    data.append(dynamic_time)
    data.append(size_of_insert)
    data.append(generation_time)
    data.append(db_size_before_insert)
    return data


def docker_reset_db():
    docker_command = "docker compose down -v && docker compose up --build -d"
    temp = os.system(docker_command)
    if temp == 0:
        print("succes")
    # doesnt work if i dont sleep :-( please fix if possible
    time.sleep(3)


def generate_insert_array(size, file, partitions):
    partitions_of_triples = []
    if size == 0:
        return partitions_of_triples
    with open(file, "r") as f:
        lines = f.readlines()
    triples = ""
    for i in range(math.ceil(size/partitions)):
        partitions_of_triples.append("INSERT DATA {" + "".join(lines[i*partitions:i+1*partitions]) + "}")

    return partitions_of_triples
    







