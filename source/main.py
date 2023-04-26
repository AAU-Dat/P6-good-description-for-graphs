from lib import *

def main():
    endpoint = "http://localhost:7200/repositories/one-million-repository"
    MakeVoidDescription()
    input_query = getQuery()
    executing_query = QueryMaker(input_query)
    print(executing_query)
    GetTimeOfQuery(endpoint, executing_query)

#Move to lib.py later
def QueryMaker(query):
    dictionary = create_dict_based_on_query(query)
    new_query = create_void_select(dictionary)
    return new_query

main()