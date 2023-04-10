from SPARQLWrapper import SPARQLWrapper, JSON, POST
from collections import Counter


# Creates a get request to the endpoint, and returns the data from the query
# Endpoint is the repository URL from GraphDB - Query is just the SparQL query
def SelectQuery(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
    except Exception as e:
        print(e)
    return ret


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
# For now we are not using the URI space, but we might need it later.
def CreateBaseVoidDescription(Title, Description, amount_of_triples, distinct_subject, distinct_objects, distinct_properties):
    dataset_uri = "http://example.com"
    uri_space = "http://example.com"

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
    predicate_dictionary = CreateUniqueOccurenceCountDictionaryionary(
        data, "p")
    object_dictionary = CreateUniqueOccurenceCountDictionaryionary(data, "o")

    return CreateBaseVoidDescription(title, description, CountTriples(data),
                                     len(subjects_dictionary),
                                     len(object_dictionary),
                                     len(predicate_dictionary))
