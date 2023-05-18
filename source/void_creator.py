import csv

from generationData import *
from lib import *


class Void_description:
    triple_count: int
    unique_subjects_count: int
    unique_predicates_count: int
    unique_objects_count: int

    def __init__(self, triples, subjects, predicates, objects):
        self.triple_count = triples
        self.unique_subjects_count = subjects
        self.unique_predicates_count = predicates
        self.unique_objects_count = objects

    def print(self):
        print(self.triple_count, "\n", self.unique_subjects_count)

    def CreateBaseVoidDescription(self, Title, dataset_uri):
        distinct_objects = self.unique_objects_count
        distinct_subject = self.unique_subjects_count
        distinct_properties = self.unique_predicates_count

        voidDescription = f"""
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix void: <http://rdfs.org/ns/void#>

        INSERT DATA{{
        <{dataset_uri}> a void:Dataset ;
            rdfs:label "{Title}" ;
            void:uriSpace "{dataset_uri}" ;
            void:triples {self.triple_count} ;
            void:entities {distinct_objects + distinct_properties + distinct_subject} ;
            void:properties {distinct_properties} ;
            void:distinctSubjects {distinct_subject} ;
            void:distinctObjects {distinct_objects} .
        }}"""
        return voidDescription

    def compare_void(self, void_description):
        if (
            self.triple_count == void_description.triple_count
            and self.unique_subjects_count == void_description.unique_subjects_count
            and self.unique_predicates_count == void_description.unique_predicates_count
            and self.unique_objects_count == void_description.unique_objects_count
        ):
            return True
        return False


def create_void_test(endpoint, db_increase_file):
    docker_reset_db()

    dyn_void_description = Void_description(0, 0, 0, 0)
    gen_void_description = Void_description(0, 0, 0, 0)
    generation_query = "SELECT (COUNT(*) AS ?totalTriples) (COUNT(DISTINCT ?subject) AS ?numSubjects) (COUNT(DISTINCT ?predicate) AS ?numPredicates) (COUNT(DISTINCT ?object) AS ?numObjects) WHERE { ?subject ?predicate ?object . }"
    initial_data_state = GetTimeOfQuery(endpoint, generation_query)
    update_void_gen(initial_data_state["dataSet"], gen_void_description)
    update_void_gen(initial_data_state["dataSet"], dyn_void_description)
    # Define the number of lines to send at a time
    chunk_size = 10000
    times_size_db = []
    dyn_times_db = []
    db_size = 1000000

    # Open the file for reading
    try:
        count = 0
        lines = []
        with open(db_increase_file, "r") as f:
            # Read the first chunk of lines
            for line in f:
                if count == 10000:
                    data = "".join(lines)
                    query = "INSERT DATA {" + data + "}"
                    query_dict = create_dict_based_on_query(query)
                    dynamic_query = create_void_select(query_dict)
                    dyn = GetTimeOfQuery(endpoint, dynamic_query)
                    InsertDataQuery(endpoint, query)
                    gen = GetTimeOfQuery(endpoint, generation_query)
                    update_void_gen(gen["dataSet"], gen_void_description)
                    update_void_dyn(dyn["dataSet"], query_dict, dyn_void_description)
                    db_size += len(lines)
                    print(db_size)
                    lines = f.readlines(chunk_size)
                    count = 0
                    lines = []
                    assert gen_void_description.compare_void(dyn_void_description)
                else:
                    lines.append(line)
                    count += 1
                if db_size > 2000000:
                    break
    except Exception as err:
        print(err)
    with open("void_description_result", "w") as file:
        file.write(
            dyn_void_description.CreateBaseVoidDescription(
                "dyn_void_description", "test.com"
            )
        )
        file.write(
            gen_void_description.CreateBaseVoidDescription(
                "gen_void_description", "test2.com"
            )
        )


def update_void_gen(response, void_descript):
    values = list(response[0].items())
    triples = int(values[0][1]["value"])
    subjects = int(values[1][1]["value"])
    predicates = int(values[2][1]["value"])
    objects = int(values[3][1]["value"])
    void_descript.triple_count = triples
    void_descript.unique_subjects_count = subjects
    void_descript.unique_predicates_count = predicates
    void_descript.unique_objects_count = objects


def update_void_dyn(response, query_dict, void_descript):
    tri = query_dict["amount_triples"]
    sub = query_dict["amount_subjects"]
    pre = query_dict["amount_predicates"]
    obj = query_dict["amount_objects"]
    values = list(response[0].items())
    count = 0
    for value in response:
        val = value["existing"]["value"]
        if sub > count:
            if val == "false":
                void_descript.unique_subjects_count += 1
                temp = void_descript.unique_subjects_count

        elif sub + pre > count:
            if val == "false":
                void_descript.unique_predicates_count += 1

        elif sub + pre + obj > count:
            if val == "false":
                void_descript.unique_objects_count += 1
        else:
            if val == "false":
                void_descript.triple_count += 1
                temp2 = void_descript.triple_count
        count += 1


create_void_test(
    "http://localhost:7200/repositories/one-million-repository",
    "database/new_size_9mil.nt",
)
