from lib import *
from generationData import *
import csv


def main(name):
    endpoint = "http://localhost:7200/repositories/one-million-repository"
    times = []
    data_labels = [
        "dynamic time in msek",
        "amount of triples inserted",
        "generation time in msek",
        "dbsize in triples",
    ]
    # input_querys = generate_query("database/two-million.nt", amount)
    # for i in range(len(input_querys)):
    #     executing_query = QueryMaker(input_querys[i])
    #     times.append(GetTimeOfQuery(endpoint, executing_query))
    #     data.append([times[i]["time in ms"], 2**i])

    data = datageneration(
        dbinc,
        1000000,
        inc,
        10000,
        endpoint,
        "database/two-million.nt",
        "database/three-million.nt",
    )
    # Open the file in write mode with the CSV writer
    print(data)
    with open(name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data_labels)
        # Write each row of the 2D array as a separate row in the CSV file
        for row in data:
            writer.writerow(row)


def inc(i):
    return 1000 + i


def dbinc(j):
    return 10000 + j
docker_reset_db()
endp = "http://localhost:7200/repositories/one-million-repository"
gen = generate_insert(100,"database/two-million.nt" )
q = QueryMaker(gen)
print(q)
dynamic_time = GetTimeOfQuery(endp, q )["time in ms"]
print(dynamic_time)
main("data4.csv")
