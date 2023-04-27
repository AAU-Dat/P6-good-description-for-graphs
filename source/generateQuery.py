path = "database/two-million.nt"

# Takes a path to the file and the number of triples to retrieve
# Retrieve the first n triples from a file and return them as a string
def retrieve_triples(file_path, num_triples, start = 0):
    with open(file_path, "r") as f:
        lines = f.readlines()
    triples = ""
    i = start
    while i <= num_triples and i < len(lines):
        line = lines[i].strip()
        triples += line
        i += 1
    return triples


# Takes a path to the file and the number of strings to retrieve
# For each string, the number of triples retrieved is 2^n - 2, 4, 8... 2^n
def array_of_triples(file_path, num_strings):
    array_of_strings = []
    i = 1
    while i <= num_strings:
        array_of_strings.append(retrieve_triples(file_path, 2**i, 2**(i-1)))
        i += 1
    return array_of_strings

# Takes a path to the file and the number of strings to retrieve
# Creates an array of strings, each string is a query to insert the triples where the number of triples increases exponentially
def generate_query(file_path, num_strings):
    array_of_strings = array_of_triples(file_path, num_strings)
    queries = []
    for i in range(len(array_of_strings)):
        queries.append("INSERT DATA {" + array_of_strings[i] + "}")
    return queries