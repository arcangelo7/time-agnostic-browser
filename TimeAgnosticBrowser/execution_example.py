from agnostic_query import Agnostic_query
from pprint import pprint

result = Agnostic_query.get_entity_history(res="https://github.com/arcangelo7/time_agnostic/ra/5")
pprint(result)