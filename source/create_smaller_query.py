import re

testquery = 'INSERT DATA { <http://example.org/person1> <http://example.org/name> "John Smith". <http://example.org/person1> <http://example.org/age> "35"^^<http://www.w3.org/2001/XMLSchema#integer> . <http://example.org/person2> <http://example.org/name> "Jane Doe" .}'

m = re.search(r'\{.*\}', testquery)
string = m.group(0)[1:-1]

print(string)
