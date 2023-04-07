from SPARQLWrapper import SPARQLWrapper, JSON

# Endpoint is the repository URL from GraphDB - Query is just the SparQL query


def PokemonQuery(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
    except Exception as e:
        print(e)
    return ret


def InsertQuery(endpoint, query):
    sparql = SPARQLWrapper(endpoint)

    sparql.setQuery(query)
    sparql.Method = 'POST'
    sparql.query()

    try:
        ret = sparql.queryAndConvert()
    except Exception as e:
        print(e)
