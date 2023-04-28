from lib import *
import csv


def main(name, amount):
    endpoint = "http://localhost:7200/repositories/one-million-repository"
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


main("hello.csv", 2)
