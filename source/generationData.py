from lib import *
import os


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
    i = 1
    j = 1
    while i < maximum_db_size_added:
        j = 1
        while j < maximum_querysize:
            docker_reset_db()
            initial_insert = generate_insert(i, db_increase_file)
            InsertDataQuery(endpoint, initial_insert)
            data.append(create_data(j, db_size + i, querysize_increase_file, endpoint))
            j = querysize_increment_func(j)
        i = database_increment_func(i)
    return data


def create_data(size_of_insert, db_size_before_insert, file_to_generate_from, endpoint):
    data = []
    generation_query = "SELECT (COUNT(*) AS ?totalTriples) (COUNT(DISTINCT ?subject) AS ?numSubjects) (COUNT(DISTINCT ?predicate) AS ?numPredicates) (COUNT(DISTINCT ?object) AS ?numObjects) WHERE { ?subject ?predicate ?object . }"
    insert_q = generate_insert(size_of_insert, file_to_generate_from)
    dynamic_time = GetTimeOfQuery(endpoint, QueryMaker(insert_q))["time in ms"]
    print("got dynamic time:", dynamic_time, "size of insert:", size_of_insert)
    InsertDataQuery(endpoint, insert_q)
    generation_time = GetTimeOfQuery(endpoint, generation_query)["time in ms"]
    print("got generation time:", generation_time)
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


# def main(name, amount):
#     endpoint = "http://localhost:7200/repositories/pokemon-repository"
#     times = []
#     data = [
#         [
#             " dynamic time in msek",
#             "amount of triples inserted",
#             "generation time in msek",
#             "dbsize in triples",
#         ]
#     ]
#     input_querys = generate_query("database/two-million.nt", amount)
#     for i in range(len(input_querys)):
#         executing_query = QueryMaker(input_querys[i])
#         print(i, "\n\n")
#         times.append(GetTimeOfQuery(endpoint, executing_query))
#         data.append([times[i]["time in ms"], 2**i])

#     mode = "w"

#     # Open the file in write mode with the CSV writer
#     with open(name, mode, newline="") as file:
#         writer = csv.writer(file)

#         # Write each row of the 2D array as a separate row in the CSV file
#         for row in data:
#             writer.writerow(row)
