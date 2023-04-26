import re

# testquery = 'INSERT DATA { <http://example.org/person1> <http://example.org/name> "John Smith". <http://example.org/person1> <http://example.org/age> "35"^^<http://www.w3.org/2001/XMLSchema#integer> . <http://example.org/person2> <http://example.org/name> "Jane Doe" .}'


def create_dict_based_on_query(query):
    m = re.search(r"\{.*\}", query)
    alltriples = m.group(0)[1:-1]

    triple_pattern = re.compile(
        r'(?:<[^>]*>|".*?"|\d+\S*)\s+(?:<[^>]*>|".*?"|\d+\S*)\s+(?:<[^>]*>|".*?"|\d+\S*)(?:\^\^<[^>]*>)?[^.]*[.]'
    )
    single = re.compile(r'(?:<[^>]*>|".*?"|\d+\S*)')

    # Use the regular expression to find all matches in the input string
    individual_triples = triple_pattern.findall(alltriples)
    print(individual_triples)
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


def create_void_select(dict):
    subjects = dict["subjects"]
    predicates = dict["predicates"]
    objects = dict["objects"]
    all_triples = dict["triples_together"]

    all_subjects = " ".join(subjects)
    all_predicates = " ".join(predicates)
    all_objects = " ".join(objects)
    first_of_query = f"{{SELECT ?resource (EXISTS {{ ?resource ?p ?o }} AS ?subject_existing) {{ VALUES ?resource {{ {all_subjects} }} }} }}"
    second_part_query = f"UNION {{ SELECT ?resource (EXISTS {{ ?s ?resource ?o }} AS ?existing) {{ VALUES ?resource {{ {all_predicates} }} }} }}"
    third_part_query = f"UNION {{ SELECT ?resource (EXISTS {{ ?s ?p ?resource }} AS ?existing) {{ VALUES ?resource {{ {all_objects} }} }} }}"
    fourth_part_query = create_fourth_part(dict["triples_individually"])
    final_query = f"SELECT * WHERE {{ {first_of_query + second_part_query + third_part_query + fourth_part_query} }}"
    return final_query


def create_fourth_part(individual_triples):
    string = ""

    for i in range(len(individual_triples)):
        string += " (" + individual_triples[i] + ") \n"
    final = f"UNION{{ SELECT DISTINCT ?triple ?exists {{ VALUES (?s ?p ?o) {{ {string} }} BIND(CONCAT(str(?s), str(?p) str(?o)) AS ?triple) BIND(EXISTS {{ ?s ?p ?o }} AS ?exists) }} }}"
    return final
