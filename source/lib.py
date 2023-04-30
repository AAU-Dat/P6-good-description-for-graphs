import json
import time
from collections import Counter
import re

from SPARQLWrapper import JSON, POST, SPARQLWrapper


# Creates a get request to the endpoint, and returns the data from the query
# Endpoint is the repository URL from GraphDB - Query is just the SparQL query
def SelectQuery(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    try:
        ret = sparql.queryAndConvert()
    except Exception as e:
        print("\n\n\nEROR\n")
        print(e)
    return ret


# Creates a get request to the endpoint, and returns the data and time from the query
def GetTimeOfQuery(endpoint, query):
    # start time and end time to calculate the time it takes to run the query
    start = time.time()
    dataSet = SelectQuery(endpoint, query)
    end = time.time()

    # create a dictionary with the data from the query and the time it took to run the query into json
    dictionary = {"dataSet": dataSet, "time in ms": (end - start) * 10**3}
    return dictionary


# Creates a post request to the endpoint, and inserts the data from the query
# Endpoint is the repository URL from GraphDB, with added "/statements" for a POST request - Query is just the SparQL query
def InsertDataQuery(endpoint, query):
    sparql = SPARQLWrapper(endpoint + "/statements")
    sparql.setMethod(POST)
    sparql.setQuery(query)
    try:
        sparql.queryAndConvert()
        print("Data inserted")
    except Exception as e:
        print(e)


# Takes a path to the file and the number of triples to retrieve
# Retrieve the first n triples from a file and return them as a string
def retrieve_triples(file_path, num_triples, start=0):
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
        array_of_strings.append(retrieve_triples(file_path, 2**i, 2 ** (i - 1)))
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


def generate_insert(size, file):
    triples = retrieve_triples(file, size)
    return "INSERT DATA {" + triples + "}"


# takes an query and creates a a dictionary that tracks the triples unique subjects predicates and objects


def create_dict_based_on_query(query):
    m = re.search(r"\{.*\}", query)
    alltriples = m.group(0)[1:-1]

    triple_pattern = re.compile(
        r'(?:<[^>]*>|".*?"|\d+\S*)\s+(?:<[^>]*>|".*?"|\d+\S*)\s+(?:<[^>]*>|".*?"|\d+\S*)(?:\^\^<[^>]*>)?[^.]*[.]'
    )
    single = re.compile(r'(?:<[^>]*>|".*?"|\d+\S*)')

    # Use the regular expression to find all matches in the input string
    individual_triples = triple_pattern.findall(alltriples)
    subject = []
    predicate = []
    object = []

    for i in range(len(individual_triples)):
        fun = single.findall(individual_triples[i])
        subject.append(fun[0])
        predicate.append(fun[1])
        object.append(fun[2])

    unique_subject = list(dict.fromkeys(subject))
    unique_predicate = list(dict.fromkeys(predicate))
    unique_object = list(dict.fromkeys(object))
    triple_dict = {
        "subjects": unique_subject,
        "predicates": unique_predicate,
        "objects": unique_object,
        "triples_together": alltriples,
        "triples_individually": individual_triples,
    }
    return triple_dict


# takes a dictionary keeping track of unique subjects predicates objects and triples from a query and creates a select query that checks if the stuff in the dict exists.


def create_void_select(dict):
    subjects = dict["subjects"]
    predicates = dict["predicates"]
    objects = dict["objects"]
    all_triples = dict["triples_together"]

    all_subjects = " ".join(subjects)
    all_predicates = " ".join(predicates)
    all_objects = " ".join(objects)
    subject_of_query = f"{{SELECT ?resource (EXISTS {{ ?resource ?p ?o }} AS ?existing) {{ VALUES ?resource {{ {all_subjects} }} }} }}"
    predicate_part_query = f"UNION {{ SELECT ?resource (EXISTS {{ ?s ?resource ?o }} AS ?existing) {{ VALUES ?resource {{ {all_predicates} }} }} }}"
    object_part_query = f"UNION {{ SELECT ?resource (EXISTS {{ ?s ?p ?resource }} AS ?existing) {{ VALUES ?resource {{ {all_objects} }} }} }}"
    triple_part_query = create_triple_part_of_query(dict["triples_individually"])
    final_query = f"SELECT * WHERE {{ {subject_of_query + predicate_part_query + object_part_query + triple_part_query} }}"
    return final_query


# creates the triple part of the select query using an array of individual triples


def create_triple_part_of_query(individual_triples):
    string = ""

    for i in range(len(individual_triples)):
        string += " (" + individual_triples[i][:-1] + ") \n"
    final = f"UNION{{ SELECT DISTINCT ?triple ?existing {{ VALUES (?s ?p ?o) {{ {string} }} BIND(CONCAT(str(?s), str(?p), str(?o)) AS ?triple) BIND(EXISTS {{ ?s ?p ?o }} AS ?existing) }} }}"
    return final


# Define a function that counts the occurrences of each element in a list
def CountElements(lst):
    counter = Counter(lst)
    return dict(counter)


# Define a function that counts the number of triples in a parsed JSON object
def CountTriples(parsed_json):
    return len(parsed_json)


# Returns a list of unique predicate values in a parsed JSON object.
def CreateUniqueOccurenceCountDictionaryionary(parsed_json, name):
    values = [d[name]["value"] for d in parsed_json]
    return CountElements(values)


# create basic VOID description as a string, using input values for the number of triples, distinct subjects, distinct objects, and distinct properties in the dataset
def CreateBaseVoidDescription(
    Title,
    Description,
    amount_of_triples,
    distinct_subject,
    distinct_objects,
    distinct_properties,
):
    dataset_uri = "http://example.com"  # TODO: Use the correct URI eventually.
    uri_space = "http://example.com"  # TODO: Use the correct URI eventually.

    voidDescription = f"""
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix void: <http://rdfs.org/ns/void#>

    INSERT DATA{{
    <{dataset_uri}> a void:Dataset ;
        rdfs:label "{Title}" ;
        void:description "{Description}" ;
        void:uriSpace "{uri_space}" ;
        void:triples {amount_of_triples} ;
        void:entities {distinct_objects + distinct_properties + distinct_subject} ;
        void:properties {distinct_properties} ;
        void:distinctSubjects {distinct_subject} ;
        void:distinctObjects {distinct_objects} .
    }}"""
    return voidDescription


# Data is the parsed JSON object from the query
# VoidCreator takes the parsed JSON object and creates a VOID description from it, that details the number of triples, distinct subjects, distinct objects, and distinct properties in the dataset
def VoidCreator(title, description, data):
    data = data["results"]["bindings"]
    subjects_dictionary = CreateUniqueOccurenceCountDictionaryionary(data, "s")
    predicate_dictionary = CreateUniqueOccurenceCountDictionaryionary(data, "p")
    object_dictionary = CreateUniqueOccurenceCountDictionaryionary(data, "o")

    return CreateBaseVoidDescription(
        title,
        description,
        CountTriples(data),
        len(subjects_dictionary),
        len(object_dictionary),
        len(predicate_dictionary),
    )


def QueryMaker(query):
    dictionary = create_dict_based_on_query(query)
    new_query = create_void_select(dictionary)
    return new_query
