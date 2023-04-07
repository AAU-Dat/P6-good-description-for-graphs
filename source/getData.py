from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

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
    sparql.setHTTPAuth(DIGEST)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    results = sparql.query()
    print(results.response.read())
