path = "database/two-million.nt"


def retrieve_triples(file_path, num_triples):
    with open(file_path, "r") as f:
        lines = f.readlines()
    triples = []
    for i in range(len(lines)):
        if len(triples) >= num_triples:
            break
        line = lines[i].strip()
        triples.append(line)
    return triples


# The amount of arrays - Where for each additional array, the number of triples is doubled - 2^n
def array_of_triples(file_path, num_arrays):
    arrayOfArrays = []
    i = 1
    while i <= num_arrays:
        arrayOfArrays.append(retrieve_triples(file_path, 2**i))
        i += 1
    return arrayOfArrays


# start from 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 triples- 2^n
arr = array_of_triples(path, 5)

for i in range(len(arr)):
    print("Array " + str(i + 1) + " size: " + str(len(arr[i])))
    print(arr[i])
