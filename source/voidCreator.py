import json
from collections import Counter


# Define a function that counts the occurrences of each element in a list
def count_elements(lst):
    counter = Counter(lst)
    return dict(counter)


# Load the JSON file
with open(
    "/home/gustav/projects/P6-good-description-for-graphs/source/query(3).json"
) as f:
    data = json.load(f)


# Define a function that counts the number of triples in a parsed JSON object
def count_triples(parsed_json):
    return len(parsed_json)


# Define a function that returns a list of unique predicate values in a parsed JSON object
# def return_predicate_list_unique(parsed_json):
#    return list(set([d["p"] for d in parsed_json]))


# Define a function that counts the number of occurrences of each unique predicate value in a parsed JSON object and returns a dictionary
def amount_of_unique_dict(parsed_json):
    return count_elements(parsed_json)


def create_unique_occurence_count_dict(parsed_json, name):
    values = [d[name] for d in data]
    return amount_of_unique_dict(values)


# Define a function that creates a basic VOID description as a string, using input values for the number of triples, distinct subjects, distinct objects, and distinct properties in the dataset
def create_base_void_description(
    amount_of_triples, distinct_subject, distinct_objects, distinct_properties
):
    dataset_uri = "http://example.com"
    title = "Example"
    description = "This is an example"
    uri_space = "http://example.com"
    num_triples = amount_of_triples

    void = f"""
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix void: <http://rdfs.org/ns/void#> .

    <{dataset_uri}> a void:Dataset ;
        rdfs:label "{title}" ;
        void:description "{description}" ;
        void:uriSpace "{uri_space}" ;
        void:entities {distinct_objects + distinct_properties + distinct_subject} ;
        void:properties {distinct_properties} ;
        void:distinctSubjects {distinct_subject} ;
        void:distinctObjects {distinct_objects}.
    """
    return void


subjects_dict = create_unique_occurence_count_dict(data, "s")
predicate_dict = create_unique_occurence_count_dict(data, "p")
object_dict = create_unique_occurence_count_dict(data, "o")


# Print some counts and the base VOID description

print(
    create_base_void_description(
        count_triples(data),
        len(subjects_dict),
        len(object_dict),
        len(predicate_dict),
    )
)
